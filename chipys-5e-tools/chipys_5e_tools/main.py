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

def apply_ui_connections(gui_obj:QT.gui.Ui_MainWindow):
    """Overlay that connects up the GUI so that we can modularly replace the gui.py from QT5

    Args:
        gui_obj (gui.Ui_MainWindow): Main window GUI object
    """
    # link buttons
    gui_obj.simulate.clicked.connect(lambda: run_sim(gui_obj))
    gui_obj.roll_active.clicked.connect(lambda: roll_active(gui_obj))

    # connect listView log to click even with index
    gui_obj.dice_log.clicked[QtCore.QModelIndex].connect(click_dice_log)
    gui_obj.formula_log.clicked[QtCore.QModelIndex].connect(click_formula_log)

def show_popup(gui_obj):
    msg = QtWidgets.QMessageBox()
    msg.setWindowTitle("Results!")
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
    flag_pam = gui_obj.flag_pam.isChecked()
  

    roll, log, formula = dice_tower.r(formula, show_rolls=True,
                                                flag_adv = flag_adv,
                                                flag_bls = flag_bls,
                                                flag_dis = flag_dis,
                                                flag_ela = flag_ela,
                                                flag_ins = flag_ins,
                                                flag_pam = flag_pam)

    # build log
    dice_log.append([formula,log])
    dice_log_model = QtGui.QStandardItemModel()
    gui_obj.dice_log.setModel(dice_log_model)
    dice_log_model.clear()
    for r in dice_log[-8:]:
        dice_log_model.appendRow(QtGui.QStandardItem(str(r)))

    # build log last used formula
    expanded_var = formula_log[-1:][0]
    if formula != expanded_var:
        formula_log.append(formula)
    formula_log_model = QtGui.QStandardItemModel()
    gui_obj.formula_log.setModel(formula_log_model)
    formula_log_model.clear()
    for r in formula_log[-8:]:
        formula_log_model.appendRow(QtGui.QStandardItem(str(r)))        

    # display the current roll results
    gui_obj.result.setText(str(roll))
    return roll
    
def run_sim(gui_obj):
    global dice_tower
    gui_obj.result.setText("Init...")
    max_roll = dice_tower.max_roll(gui_obj.attack_formula.text())
    roll_tally = [0 for i in range(max_roll)]
    sim_count = gui_obj.sim_count.text()
    print(sim_count)

    for i in range(int(sim_count)):
        rolled = roll_active(gui_obj)
        # print(roll_tally)
        roll_tally[rolled-1] += 1
    
    print(roll_tally)
    print([round((roll_tally[i]/int(sim_count))*100,1) for i in range(max_roll)])
    gui_obj.result.setText("Done!")
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = QT.gui.Ui_MainWindow()
    ui.setupUi(MainWindow)
    apply_ui_connections(ui)  # here we modify actions to the GUI
    MainWindow.show()
    sys.exit(app.exec_())