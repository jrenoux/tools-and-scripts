# LaTeX Custom Compiling with Automatic Reference Grabber

This script provide a complete compilation line for your latex project with automatic referrences grabber. It performs the following operations in order: 
1. Gather references from your text. More specifically : 
   - It finds all your citation commands in your tex file.
   - It fetches the corresponding reference from your master bib file, and append it in a local bib file for your tex project
   - If any references exist in your local bib file but not in your master file, these references will be stored in a separate file called `missing-from-master.bib`, situated in your project folder.
3. Compile your latex project according to the standard tex-bib-tex-tex compile chain. 
4. Show you the remaining warning at the end of the compilation
5. Grabs all instances of `TODO` in your tex file and display them as a summary at the end of the compilation. 


## Requirements
1. On single master bib file containing all your references
2. Python 3

## Script Configuration
In `compile_latex.sh`, indicate: 
1. The path to your master bib file
2. The path to your current folder (necessary to fetch the master filename)
3. Ensure that `compile_latex.sh` is executable

## Usage
You can call the script as follows: 
`./compile_latex.sh [*biber/*bibtex] filename`

If you don't specify an option for biber/bibtex, the default engine is biber. 

You may also call the script on any tex sub-file, at the condition that you add the following lines at the end of your file: 

```
%%% Local Variables:
%%% mode: latex
%%% TeX-master: "your-main-tex-file-name"
%%% End:
```
The script will create a folder called `your-project.build` containing all the build files. 

Local changes made to your local bib file will *not* be overridden. 



## Emacs Configuration (Optional)
If you're an Emacs user, you may want to add the following custom functions to your initialization file to be able to call the script from your tex buffer (don't forget to change the paths)

```
(defun tex-custom-compile-biber (arg)
  (interactive "P")
  "Calls `<path-to-root-folder>/compile_latex.sh biber' on file associated with current buffer."
  (let (script texFile)

   (setq script "<path-to-root-folder>compile_latex.sh biber  ")
  

    (async-shell-command 
     (concat
      script
      (buffer-file-name)
     )
    )
  )
)

(eval-after-load "tex"
  '(define-key TeX-mode-map (kbd "C-c C-t C-a") 'tex-custom-compile-biber))


(defun tex-custom-compile-bibtex (arg)
  (interactive "P")
  "Calls `<path-to-root-folder>/compile_latex.sh bibtex' on file associated with current buffer."
  (let (script texFile)

   (setq script "<path-to-root-folder>/compile_latex.sh bibtex  ")
  

    (async-shell-command 
     (concat
      script
      (buffer-file-name)
     )
    )
  )
)

(eval-after-load "tex"
  '(define-key TeX-mode-map (kbd "C-c C-t C-x") 'tex-custom-compile-bibtex))

```


## Known issues and missing features
1. The code crashes in multi-folder projects with custom style files if you compile from a sub-folder. In these cases, always compile from the root folder. 
2. For now only some biblatex citation styles are supported for automatic references grabbing. Using other citation style will not make the script crash but won't activate the reference grabber. For now, the script supports `cite`, `citep`, `citet`, `textcite`. 
3. Changes in your master bib file are not automatically reflected in the local bib file and requires you to delete the local bib to recreate it. 
