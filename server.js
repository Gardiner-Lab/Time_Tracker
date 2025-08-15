const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const bodyParser = require('body-parser');
const path = require('path');
const fs = require('fs');

const app = express();
const port = 5000;
// Use data directory for database persistence in Docker
const dbPath = process.env.NODE_ENV === 'production' ? './data/database.db' : './database.db';
const db = new sqlite3.Database(dbPath);

app.use(bodyParser.json());

// Set Content Security Policy headers
app.use((req, res, next) => {
    res.setHeader("Content-Security-Policy", "default-src 'self'; img-src 'self' data:; script-src 'self' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline'; connect-src 'self'");
    next();
});

// Handle favicon requests
app.get('/favicon.ico', (req, res) => {
    res.status(204).end();
});

// Create tables synchronously before starting server
db.serialize(() => {
  db.run(`CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
  )`);

  db.run(`CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    group_id INTEGER,
    FOREIGN KEY(group_id) REFERENCES groups(id)
  )`);

  db.run(`CREATE TABLE IF NOT EXISTS time_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME,
    duration INTEGER,
    note TEXT,
    period_id INTEGER,
    FOREIGN KEY(task_id) REFERENCES tasks(id)
  )`);

  db.run(`CREATE TABLE IF NOT EXISTS academic_periods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL
  )`);
  
  // Start server AFTER tables are created
  const server = app.listen(port, () => console.log(`Server running on port ${port}`));
  
  // Add shutdown endpoint
  app.get('/shutdown', (req, res) => {
      res.json({ success: true });
      console.log("Shutting down server...");
      server.close(() => {
          process.exit(0);
      });
  });
});

// Academic Period endpoints
app.get('/periods', (_, res) => {
  db.all('SELECT * FROM academic_periods', (err, rows) => {
    if (err) return res.status(500).send(err.message);
    res.json(rows);
  });
});

app.post('/periods', (req, res) => {
  const { name, start_date, end_date } = req.body;
  db.run('INSERT INTO academic_periods (name, start_date, end_date) VALUES (?, ?, ?)', 
    [name, start_date, end_date], function(err) {
      if (err) return res.status(500).send(err.message);
      res.json({ id: this.lastID, name, start_date, end_date });
  });
});

// Group endpoints
app.post('/groups', (req, res) => {
  const { name } = req.body;
  db.run('INSERT INTO groups (name) VALUES (?)', [name], function(err) {
    if (err) return res.status(500).send(err.message);
    res.json({ id: this.lastID, name });
  });
});

app.get('/groups', (_, res) => {
  db.all('SELECT * FROM groups', (err, rows) => {
    if (err) return res.status(500).send(err.message);
    res.json(rows);
  });
});

// Task endpoints
app.post('/tasks', (req, res) => {
  const { name, group_id } = req.body;
  db.run('INSERT INTO tasks (name, group_id) VALUES (?, ?)', [name, group_id], 
    function(err) {
      if (err) return res.status(500).send(err.message);
      res.json({ id: this.lastID, name, group_id });
  });
});

// Timer endpoints
app.post('/timer/start', (req, res) => {
  const { task_id } = req.body;
  const start_time = new Date().toISOString();
  db.run('INSERT INTO time_entries (task_id, start_time) VALUES (?, ?)', [task_id, start_time],
    function(err) {
      if (err) return res.status(500).send(err.message);
      res.json({ id: this.lastID });
  });
});

app.post('/timer/stop', (req, res) => {
  const { id, note } = req.body;
  const end_time = new Date();
  
  db.get('SELECT start_time FROM time_entries WHERE id = ?', [id], (err, row) => {
    if (err) return res.status(500).send(err.message);
    
    const start = new Date(row.start_time);
    const duration = Math.floor((end_time - start) / 1000); // seconds
    
    db.run('UPDATE time_entries SET end_time = ?, duration = ?, note = ? WHERE id = ?',
      [end_time.toISOString(), duration, note || "", id],
      function(err) {
        if (err) return res.status(500).send(err.message);
        res.json({ duration });
      }
    );
  });
});

app.get('/tasks', (req, res) => {
  const group_id = req.query.group_id;
  if (!group_id) return res.status(400).send("group_id is required");
  
  const query = `
    SELECT 
      tasks.id, 
      tasks.name,
      ROUND(COALESCE(SUM(time_entries.duration), 0) / 3600.0, 2) AS total_hours,
      ROUND(COALESCE(SUM(time_entries.duration), 0) / 3600.0 / 7, 2) AS hours_per_week
    FROM tasks
    LEFT JOIN time_entries ON tasks.id = time_entries.task_id
    WHERE tasks.group_id = ?
    GROUP BY tasks.id
  `;
  
  db.all(query, [group_id], (err, rows) => {
    if (err) return res.status(500).send(err.message);
    res.json(rows);
  });
});

app.get('/time_entries', (req, res) => {
  const task_id = req.query.task_id;
  db.all('SELECT id, task_id, start_time, end_time, duration, note FROM time_entries WHERE task_id = ?', [task_id], (err, rows) => {
    if (err) return res.status(500).send(err.message);
    res.json(rows);
  });
});

// Time by group endpoint
app.get('/time_by_group', (req, res) => {
  const query = `
    SELECT 
      groups.id, 
      groups.name,
      ROUND(COALESCE(SUM(time_entries.duration), 0) / 3600.0, 2) AS total_time,
      ROUND(COALESCE(SUM(time_entries.duration), 0) / 3600.0 / 7, 2) AS hours_per_week
    FROM groups
    LEFT JOIN tasks ON groups.id = tasks.group_id
    LEFT JOIN time_entries ON tasks.id = time_entries.task_id
    GROUP BY groups.id
  `;
  
  db.all(query, (err, rows) => {
    if (err) {
      console.error(err);
      return res.status(500).send(err.message);
    }
    res.json(rows);
  });
});

// Delete group endpoint
app.delete('/groups/:id', (req, res) => {
  const { id } = req.params;
  db.run('DELETE FROM groups WHERE id = ?', [id], function(err) {
    if (err) return res.status(500).send(err.message);
    if (this.changes === 0) return res.status(404).send("Group not found");
    res.json({ success: true });
  });
});

// Delete task endpoint
app.delete('/tasks/:id', (req, res) => {
  const { id } = req.params;
  db.run('DELETE FROM tasks WHERE id = ?', [id], function(err) {
    if (err) return res.status(500).send(err.message);
    if (this.changes === 0) return res.status(404).send("Task not found");
    res.json({ success: true });
  });
});

// Delete time entry endpoint
app.delete('/time_entries/:id', (req, res) => {
  const { id } = req.params;
  db.run('DELETE FROM time_entries WHERE id = ?', [id], function(err) {
    if (err) return res.status(500).send(err.message);
    if (this.changes === 0) return res.status(404).send("Time entry not found");
    res.json({ success: true });
  });
});

// Get all tasks without filtering
app.get('/all_tasks', (req, res) => {
  db.all('SELECT * FROM tasks', (err, rows) => {
    if (err) return res.status(500).send(err.message);
    res.json(rows);
  });
});

// Get all time entries without filtering
app.get('/all_time_entries', (req, res) => {
  db.all('SELECT * FROM time_entries', (err, rows) => {
    if (err) return res.status(500).send(err.message);
    res.json(rows);
  });
});

// Delete period endpoint
app.delete('/periods/:id', (req, res) => {
  const { id } = req.params;
  db.run('DELETE FROM academic_periods WHERE id = ?', [id], function(err) {
    if (err) return res.status(500).send(err.message);
    if (this.changes === 0) return res.status(404).send("Period not found");
    res.json({ success: true });
  });
});

// Time by task endpoint
app.get('/time_by_task', (req, res) => {
  const group_id = req.query.group_id;
  
  let query = `
    SELECT 
      tasks.id, 
      tasks.name,
      ROUND(COALESCE(SUM(time_entries.duration), 0) / 3600.0, 2) AS total_time,
      ROUND(COALESCE(SUM(time_entries.duration), 0) / 3600.0 / 7, 2) AS hours_per_week
    FROM tasks
    LEFT JOIN time_entries ON tasks.id = time_entries.task_id
  `;

  const params = [];
  if (group_id) {
    query += ' WHERE tasks.group_id = ? ';
    params.push(group_id);
  }

  query += ' GROUP BY tasks.id ';

  db.all(query, params, (err, rows) => {
    if (err) {
      console.error(err);
      return res.status(500).send(err.message);
    }
    res.json(rows);
  });
});

