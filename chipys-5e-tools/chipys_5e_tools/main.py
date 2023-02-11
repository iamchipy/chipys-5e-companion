from PyQt5 import QtCore, QtGui, QtWidgets
import QT.gui
import sys
import dice

# define globals
formula_log = [""]
formula_log_model = None
dice_log = []
dice_log_model = None
ui = None
dice_tower = dice.Dice()

def apply_ui_connections(gui_obj:QT.gui.Ui_MainWindow, win_hndl:QtWidgets.QMainWindow):
    """Overlay that connects up the GUI so that we can modularly replace the gui.py from QT5

    Args:
        gui_obj (gui.Ui_MainWindow): Main window GUI object
    """
    # set window icon
    win_hndl.setWindowIcon(QtGui.QIcon('Chipy128.ico'))
    win_hndl.setWindowTitle("Chipy's 5E Dice Sim")

    # link menus
    gui_obj.actionProject_GitHub.triggered.connect(lambda: show_popup("Thanks for your curiosity! Please feel free to check out the project at https://github.com/iamchipy/chipys-5e-companion"))
    gui_obj.actionChipy_Dev.triggered.connect(lambda: show_popup("Thanks for your curiosity! You can find more of my stuff at www.chipy.dev"))

    # link buttons
    gui_obj.simulate.clicked.connect(lambda: run_sim(gui_obj))
    gui_obj.roll_active.clicked.connect(lambda: roll_active(gui_obj))

    # connect listView log to click even with index
    gui_obj.dice_log.clicked[QtCore.QModelIndex].connect(click_dice_log)
    gui_obj.formula_log.clicked[QtCore.QModelIndex].connect(click_formula_log)

def show_popup( in_str):
    msg = QtWidgets.QMessageBox()
    msg.setWindowTitle("Results!")
    msg.setText(in_str)
    # msg.setIcon()
    msg_instance = msg.exec_()  # exec with instanciation

def click_dice_log(index):
    global dice_log_model, ui
    item = dice_log_model.itemFromIndex(index)
    log_str = str(item.text())
    log_list = log_str.split("'")
    formula_used_was = log_list[1]
    ui.attack_formula.setText(formula_used_was)

def click_formula_log(index):
    global formula_log_model, ui
    item = formula_log_model.itemFromIndex(index)
    formula_used_was = str(item.text())
    ui.attack_formula.setText(formula_used_was)    

def roll_active(gui_obj):
    global dice_log, dice_log_model, formula_log, formula_log_model
    dice_tower = dice.Dice()
    formula = gui_obj.attack_formula.text()
    flag_adv = gui_obj.flag_adv.isChecked()
    flag_bls = gui_obj.flag_bls.isChecked()
    flag_dis = gui_obj.flag_dis.isChecked()
    flag_ela = gui_obj.flag_ela.isChecked()
    flag_ins = gui_obj.flag_ins.isChecked()
    flag_gwm = gui_obj.flag_gwm.isChecked()
    ac= gui_obj.armor_class.value()
    hit_rate = [0,0]
  

    roll, log, formula = dice_tower.r(formula, show_rolls=True,
                                                flag_adv = flag_adv,
                                                flag_bls = flag_bls,
                                                flag_dis = flag_dis,
                                                flag_ela = flag_ela,
                                                flag_ins = flag_ins,
                                                flag_gwm = flag_gwm)

    # build log
    dice_log.append([formula,roll,log])
    dice_log_model = QtGui.QStandardItemModel()
    gui_obj.dice_log.setModel(dice_log_model)
    dice_log_model.clear()
    for r in dice_log[-8:]:
        dice_log_model.appendRow(QtGui.QStandardItem(str(r)))
        # log hits
        if  int(r[1]) > ac:
            hit_rate[0] +=1
        hit_rate[1] +=1

    # build log last used formula
    expanded_var = formula_log[-1:][0]
    if formula != expanded_var:
        formula_log.append(formula)
    formula_log_model = QtGui.QStandardItemModel()
    gui_obj.formula_log.setModel(formula_log_model)
    formula_log_model.clear()
    for r in formula_log[-8:]:
        formula_log_model.appendRow(QtGui.QStandardItem(str(r)))        

    # build hit rate
    hit_rate = (100*hit_rate[0])//hit_rate[1]

    # display the current roll results
    gui_obj.result.setText(str(roll))
    gui_obj.hit_chance.setText(str(hit_rate))
    return roll
    
def run_sim(gui_obj):
    global dice_tower
    gui_obj.result.setText("Init...")
    max_roll = dice_tower.max_roll(gui_obj.attack_formula.text())
    roll_tally = [0 for i in range(max_roll)]
    hit_tally = [0 for i in range(35)]
    sim_count = gui_obj.sim_count.text()
    ac= gui_obj.armor_class.value()
    print(f"Starting {sim_count} itterations...")

    for i in range(int(sim_count)):
    # for i in range(1000):
        # roll dice
        rolled = roll_active(gui_obj)
        
        # log the roll in our tallies
        roll_tally[rolled-1] += 1
        if ac <0:
            for dc in range(len(hit_tally)):
                if rolled >= dc:
                    hit_tally[dc-1] +=1
        elif rolled >= ac:
            hit_tally[ac-1] += 1

    roll_tally = roll_tally[1:]
    print("How hard did you hit:")
    print(roll_tally)
    print([round((roll_tally[i]/int(sim_count))*100,1) for i in range(max_roll-1)])

    hit_tally = hit_tally[:-1]
    print("How often did you hit(at what AC):")
    print(hit_tally)
    print([round((hit_tally[i]/int(sim_count))*100,1) for i in range(len(hit_tally))])    
    gui_obj.result.setText("Done!")
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = QT.gui.Ui_MainWindow()
    ui.setupUi(MainWindow)
    apply_ui_connections(ui, MainWindow)  # here we modify actions to the GUI
    MainWindow.show()
    sys.exit(app.exec_())