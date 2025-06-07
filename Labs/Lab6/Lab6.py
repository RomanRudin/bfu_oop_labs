from v_keyboard import VirtualKeyboard
from commands import PrintCharCommand

COLORING = "\033[{}m{}\033[0m"

if __name__ == "__main__":
    keyboard = VirtualKeyboard()
    
    if not keyboard.load_state():
        print(COLORING.format(33, "No saved state found, using defaults"))
    else:
        print(COLORING.format(33, "Keyboard state loaded"))
        print(COLORING.format(33, PrintCharCommand.text))
    
    with open("Labs/Lab6/data/keyboard_log.txt", "w") as log_file:
        def print_and_log(message) -> None:
            print(COLORING.format(32, message))
            log_file.write(message + "\n")
        
        print_and_log(keyboard.press_key("a"))
        print_and_log(keyboard.press_key("b"))
        print_and_log(keyboard.press_key("c"))
        print_and_log(keyboard.press_key("undo"))
        print_and_log(keyboard.press_key("undo"))
        print_and_log(keyboard.press_key("redo"))
        print_and_log(keyboard.press_key("ctrl++"))
        print_and_log(keyboard.press_key("ctrl+-"))
        print_and_log(keyboard.press_key("ctrl+p"))
        print_and_log(keyboard.press_key("d"))
        print_and_log(keyboard.press_key("undo"))
        print_and_log(keyboard.press_key("undo"))
        
        keyboard.save_state()
        print_and_log("Keyboard state saved")
