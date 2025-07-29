
namespace eval ttk::theme::azure {
    variable colors
    array set colors {
        -fg             "#ffffff"
        -bg             "#333333"
        -disabledfg     "#aaaaaa"
        -disabledbg     "#444444"
        -selectfg       "#ffffff"
        -selectbg       "#0078d7"
    }

    ttk::style theme create azure -parent default -settings {
        ttk::style configure .             -background $colors(-bg)             -foreground $colors(-fg)             -troughcolor $colors(-bg)             -focuscolor $colors(-selectbg)             -selectbackground $colors(-selectbg)             -selectforeground $colors(-selectfg)             -insertwidth 1             -insertcolor $colors(-fg)             -fieldbackground $colors(-bg)             -font {"Segoe Ui" 10}             -borderwidth 1             -relief flat

        ttk::style map . -foreground [list disabled $colors(-disabledfg)]
        ttk::style map . -background [list disabled $colors(-disabledbg)]
        
        ttk::style configure TButton -padding {15 5} -anchor center
        ttk::style configure Treeview.Heading -font {"Segoe Ui" 10 bold}
        ttk::style configure Treeview -font {"Segoe Ui" 10} -rowheight 25
        ttk::style configure TLabelframe.Label -font {"Segoe Ui" 11 bold}
    }
}
