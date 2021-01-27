(TeX-add-style-hook
 "thesis"
 (lambda ()
   (setq TeX-command-extra-options
         "-shell-escape")
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("scrbook" "12pt" "a4paper" "oneside" "openright")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("setspace" "onehalfspacing") ("geometry" "left=4cm" "right=3cm" "top=3cm" "bottom=3cm") ("babel" "ngerman" "english") ("csquotes" "autopunct") ("datetime2" "useregional") ("biblatex" "style=authoryear-icomp" "ibidtracker=strict" "backend=biber" "")))
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "path")
   (TeX-run-style-hooks
    "latex2e"
    "scrbook"
    "scrbook12"
    "setspace"
    "geometry"
    "babel"
    "fontspec"
    "csquotes"
    "datetime2"
    "biblatex"
    "mystyle")
   (LaTeX-add-bibliographies))
 :latex)

