#fix editting to dissallow empty text field
define title = VariableInputValue(variable = "quiz_title", returnable = True)
define keys = VariableInputValue(variable = "keywords", returnable = True)

init python:
    global in_edit_title
    global in_edit_keywords
    in_edit_title = False
    in_edit_keywords = False
    global keywords

label quit_warning:
    #checks if questions are generated
    if is_notes():
        $ show_s("preprocess_text_dull")
        show halfblack
        call screen warning
    else:
        $ del_json()
        $ quiz_title = f"Quiz {persistent.quiz_def_num}" #resets
        call screen custom_quizzes

    screen warning:
        frame:
            xalign 0.5
            yalign 0.5
            xpadding 40
            ypadding 40
            xsize 450
            ysize 420
            background "#D9D9D9"

            vbox:
                xalign 0.5
                yalign 0.5

                text f"'{quiz_title}' is not yet created.":
                    font "Copperplate Gothic Thirty-Three Regular.otf"
                    size 50
                    color "#303031"
                    xalign 0.5
                    yalign 0.5
                text "Would you like to exit?":
                    font "Copperplate Gothic Thirty-Three Regular.otf"
                    size 30
                    color "#303031"
                    yoffset 10

                hbox:
                    xalign 0.5
                    yalign 0.5
                    yoffset 50
                    spacing 40

                    imagebutton auto "images/Button/yes_%s.png" action [Hide("warning"), Function(set_bool, True), Jump("warning_2")] #Function(set_bool, True) apparently was not necessary tangina
                    imagebutton auto "images/Button/no_%s.png" action [Hide("warning"), Function(set_bool, False), Jump("warning_2")]

label warning_2:
    $ hide_s("preprocess_text_dull")
    hide halfblack

    #if player wants to exit
    if bool:
        $ file_path = f"kodigo/game/python/docs/{quiz_title}.txt"
        $ file_path_json = f"kodigo/game/python/docs/{quiz_title}.json"
        $ file_path_keys = f"kodigo/game/python/docs/{quiz_title}_keys.json"

        if os.path.exists(file_path):
            $ os.remove(file_path) # remove notes
        if os.path.exists(file_path_json):
            $ os.remove(file_path_json)
        if os.path.exists(file_path_keys):
            $ os.remove(file_path_keys)
        call screen custom_quizzes with dissolve
    else:
        call screen preprocess_text

screen input_title:
    if not in_save:
        hbox:
            xalign 0.690
            yalign 0.15

            input value title length 18 allow "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789- ":
                font "Copperplate Gothic Thirty-Three Regular.otf"
                size 70
                color "#FFFFFF"
            imagebutton auto "images/Button/edit_title_%s.png" action [Hide("input_title"), Jump("edit_title_2")]:
                xoffset 40
    else:
        hbox:
            xalign 0.5
            yalign 0.1
            input value title length 18 allow "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789- ":
                xalign 0.5
                yalign 0.1
                font "Copperplate Gothic Thirty-Three Regular.otf"
                size 150
                color "#FFFFFF"
            imagebutton auto "images/Button/edit_title_%s.png" action [Hide("input_title"), Jump("edit_title_2")]:
                xoffset 40
                yoffset 45

label edit_title:
    $ in_edit_title = True

    if not in_save:
        $ show_s("preprocess_text_dull")
        hide screen preprocess_text
    else:
        hide screen save_quiz
        $ show_s("save_quiz_dull")

    $ old_fp = get_path(f"kodigo/game/python/docs/{quiz_title}.json")
    call screen input_title

label edit_title_2:
    $ new_fp = get_path(f"kodigo/game/python/docs/{quiz_title}.json")

    screen duplicate:
        vbox:
            xalign 0.5
            yalign 0.5
            xsize 1000
            ysize 100
            spacing 5
            text "Can't have multiple quizzes with the same name.":
                font "Copperplate Gothic Thirty-Three Regular.otf"
                size 60
                color "#999999"
                xalign 0.5
                yalign 0.5
            text "Try again.":
                font "Copperplate Gothic Thirty-Three Regular.otf"
                size 60
                color "#999999"
                xalign 0.5
                yalign 0.5

    #duplicate name
    if os.path.exists(new_fp) and old_fp != new_fp:
        show screen duplicate
        pause 2.0
        hide screen duplicate
        $ hide_s("preprocess_text_dull")
        call screen preprocess_text
    elif os.path.exists(old_fp):
        $ os.rename(old_fp, new_fp)
        $ fp = get_path(f"kodigo/game/python/docs/{quiz_title}.json") #reset

    $ in_edit_title = False

    if not in_save:
        $ hide_s("preprocess_text_dull")
        call screen preprocess_text
    else:
        $ hide_s("save_quiz_dull")
        call screen save_quiz

screen input_keys:
    imagebutton auto "images/Button/edit_%s.png":
        xalign 0.85
        yalign 0.5

    vbox:
        xalign 0.737
        yalign 0.4

        text "Keywords":
            font "Copperplate Gothic Thirty-Three Regular.otf"
            size 48
            color "#FFFFFF"
            xalign 0.5
            yalign 0.5

        frame:
            xalign 0.25
            yalign 0.5
            xsize 400
            ysize 400
            background "#D9D9D9"
            yoffset 30

            if keywords:
                vpgrid:
                    cols 1
                    scrollbars "vertical"
                    spacing 5
                    mousewheel True

                    vbox:
                        xsize 370
                        ysize 390
                        input value keys length 6262 allow "abcdefghijklmnopqrstuvwxyz, " multiline True:
                            font "KronaOne-Regular.ttf"
                            size 24
                            color "#303031"

label edit_keywords:
    $ keywords = get_str(get_keys())
    $ in_edit_keywords = True
    $ show_s("preprocess_text_dull")
    call screen input_keys
    $ in_edit_keywords = False
    call screen preprocess_text

screen save_quiz_dull:
    add "bg quiz main"

    imagebutton auto "images/Minigames Menu/exit_%s.png":
        xalign 0.86
        yalign 0.04

    if not in_edit_title:
        hbox:
            xalign 0.5
            yalign 0.1
            text "[quiz_title]": #specify with a number later
                font "Copperplate Gothic Thirty-Three Regular.otf"
                size 150
                color "#FFFFFF"

            imagebutton auto "images/Button/edit_title_%s.png":
                xoffset 40
                yoffset 45

screen preprocess_text_dull:
    add "bg quiz main"

    imagebutton auto "images/Minigames Menu/exit_%s.png":
        xalign 0.86
        yalign 0.04

    #get the notes if it exists
    $ notes = get_notes()
    $ keywords = get_str(get_keys())

    text "Notes":
        font "Copperplate Gothic Thirty-Three Regular.otf"
        size 48
        color "#FFFFFF"
        xalign 0.324
        yalign 0.15

    frame:
        xalign 0.25
        yalign 0.5
        xsize 600
        ysize 600
        background "#D9D9D9"


        vpgrid:
            cols 1
            scrollbars "vertical"
            spacing 5
            mousewheel True

            vbox:
                xsize 570
                ysize 590
                if notes:
                    text notes style "notes_style"
                else:
                    text "Texts from the document will appear here." style "notes_style"

    if notes:
        imagebutton auto "images/Button/summarize_%s.png":
            xalign 0.28
            yalign 0.85

    if not in_edit_keywords:
        if keywords:
            imagebutton auto "images/Button/edit_%s.png":
                xalign 0.85
                yalign 0.5

        vbox:
            xalign 0.737
            yalign 0.4

            text "Keywords":
                font "Copperplate Gothic Thirty-Three Regular.otf"
                size 48
                color "#FFFFFF"
                xalign 0.5
                yalign 0.5

            frame:
                xalign 0.25
                yalign 0.5
                xsize 400
                ysize 400
                background "#D9D9D9"
                yoffset 30

                vpgrid:
                    cols 1
                    scrollbars "vertical"
                    spacing 5
                    mousewheel True

                    vbox:
                        xsize 370
                        ysize 390
                        if keywords:
                            text keywords:
                                font "KronaOne-Regular.ttf"
                                size 24
                                color "#303031"
                        else:
                            text "Keywords from the text will appear here." style "notes_style"
    if not in_edit_title:
        hbox:
            xalign 0.690
            yalign 0.15

            text "[quiz_title]": #specify with a number later
                font "Copperplate Gothic Thirty-Three Regular.otf"
                size 70
                color "#FFFFFF"

            imagebutton auto "images/Button/edit_title_%s.png":
                xoffset 40

    if not notes:
        imagebutton auto "images/Button/upload_%s.png":
            xalign 0.75
            yalign 0.8
    else:
        imagebutton auto "images/Button/create_quiz_%s.png": #since we are skipping editting the keywords & texts, we proceed here next
            xalign 0.75
            yalign 0.8
