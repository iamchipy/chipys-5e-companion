import random as rng

def __init__():
    pass

class Dice:
    """General dice object to collect and run dice formulas 
    """
    def __init__(self):
        pass

    def r(self, in_str:str="1d20", flag_adv:bool=False, show_rolls:bool= False, flag_bls:bool= False,flag_dis:bool= False,flag_ela:bool= False,flag_ins:bool= False,flag_gwm:bool= False, flag_spec:int=0):
        """"alias for self.formula()"""
        return self.formula(in_str, flag_adv, show_rolls, flag_bls, flag_dis, flag_ela, flag_ins, flag_gwm, flag_spec)

    def f(self, in_str:str="1d20", flag_adv:bool=False, show_rolls:bool= False,flag_bls:bool= False,flag_dis:bool= False,flag_ela:bool= False,flag_ins:bool= False,flag_gwm:bool= False, flag_spec:int=0):
        """"alias for self.formula()"""
        return self.formula(in_str, flag_adv, show_rolls, flag_bls, flag_dis, flag_ela, flag_ins, flag_gwm, flag_spec)

    def formula(self, in_str:str="1d20", flag_adv:bool=False, show_rolls:bool= False, flag_bls:bool= False,flag_dis:bool= False,flag_ela:bool= False,flag_ins:bool= False,flag_gwm:bool= False, flag_spec:int=0):
        """_summary_

        Args:
            in_str (str, optional): Desired dice-formula to roll written in the #d##+#d##+# format. EXAMPLE: 1d20+2d4+3 Defaults to "1d20".
            advantage (bool, optional): When True the first dice in the formula will get one additional roll and the lower will be dropped. So "2d20" would become 3x d20 rolls with the lowest dropped. Defaults to False.
            show_rolls (bool, optional): When True return value will be an array including each dice roll and the originating formula. Defaults to False.

        Returns:
            int or list: depending on "show_rolls" flag will either return a single int value or a list [value,["each","dice","roll"],"formula given"]
        """
        dice_report= ""
        adv_rolled = False
        int_value = 0
        formula = in_str.split("+")  # | (pipe) separates delimiters
        # Blessed gets handled here ------------- flag_bls
        if flag_bls:
            formula.append("1d4")
            
        for element in formula:
            if "d" in element:
                # Advantage get handled here ------------- flag_adv
                # Disadvantage get handled here ------------- flag_dis
                # ElvenAccuracy get handled here ------------- flag_ela
                # Inspiration get handled here ------------- flag_ins

                # all of these are only being applied to the first dice in the formula and only once 
                if not adv_rolled:
                    i, s = self.roll(element, flag_adv=flag_adv, flag_dis=flag_dis, flag_ins=flag_ins, flag_ela=flag_ela)
                    dice_report += str(s)
                    int_value += i
                    adv_rolled = True
                else:
                    i, s = self.roll(element)
                    dice_report += str(s)
                    int_value += i                    
            else:
                int_value += int(element)

        # SharpShooter/GreatWepMaster gets handled here ------------- flag_gwm
        if flag_gwm:
            int_value -= 5

        # SPECIAL gets handled here ------------- flag_gwm
        int_value += flag_spec            
        
        # check what info to return and return it
        if show_rolls:
            return int_value, dice_report, in_str
        else:
            return int_value
    
    def roll(self, dice_string="1d20", flag_adv:bool=False, flag_dis:bool=False, flag_ins:bool=False, flag_ela:bool=False)-> int:
        """_summary_

        Args:
            dice_string (str, optional): Dice formula. Defaults to "1d20".
            flag_adv (bool, optional): A toggle indicating if there should be advantage (it'll roll one extra dice and drop lowest). Defaults to False.
            flag_dis (bool, optional): A toggle indicating if there should be disadvantage (it'll roll one extra dice and drop highest). Defaults to False.
            flag_ins (bool, optional): A toggle indicating if there should be advantage (it'll roll one extra dice and drop lowest). Defaults to False.
            flag_ela (bool, optional): A toggle to roll a unique stacking advantage. Defaults to False.

        Returns:
            int: dice roll
        """
        # calc advantange
        adv_counter = 0
        if flag_adv or flag_ins:
            adv_counter +=1
        if flag_dis:
            adv_counter -=1          

        adv_rolled = False
        dice_rolls = []
        kept_rolls = []
        dice_array = dice_string.split("d")
        # loop ones for each dice being roll 
        for i in range(int(dice_array[0])):
            # base dice
            dice_rolls.append(self._roll_value(dice_array[1]))
            kept_rolls = dice_rolls

            # if we've not yet rolled advantages for this dice formula yet (can't only get one adv)
            # we do this on the first roll so that we can manipulate the list safely
            if not adv_rolled:
                # if there are adv/dis to be applied roll a second dice
                if adv_counter!=0:
                    dice_rolls.append(self._roll_value(dice_array[1]))
                    adv_rolled = True
                    # if we have positive advantage then drop lower of the two
                    if adv_counter>0:
                        # if we have Elven Accuracy we do a 3rd dice and drop lowest
                        if flag_ela:
                            dice_rolls.append(self._roll_value(dice_array[1]))
                            dice_rolls.sort()
                            kept_rolls = dice_rolls[2:]
                        else:
                            dice_rolls.sort()
                            kept_rolls = dice_rolls[1:]
                    else:
                        dice_rolls.sort()
                        kept_rolls = dice_rolls[:1]                     

        return sum(kept_rolls), dice_rolls

    def _roll_value(self, sides_to_roll=0):
        """Most basic roll command to generate a random number within the range

        Returns:
            int: face value of this roll
        """
        if not sides_to_roll:
            sides_to_roll = self.sides
        return int(rng.randrange(1,int(sides_to_roll)+1))

    def max_roll(self, formula):
        parts= formula.split("+")
        max = 0
        for item in parts:
            if "d" in item:
                d = item.split("d")
                max+=(int(d[0])*int(d[1]))
            else:
                max+=int(item)
        return max


if __name__ == "__main__":
    d = Dice()
    print("1d20 ", d.r("1d20"))
    print("1d20+1 ", d.r("1d20+1"))
    print("2d20 ", d.r("2d20"))
    print("2d20 a", d.r("2d20",True))
    print("2d20 a", d.r("2d20",True,True))
    print("2d20 a", d.r("4d20",show_rolls=True, flag_adv=1, flag_ela=1))
    print("1d20 ", d.r("1d20",show_rolls=1,flag_gwm=1))
    print("1d20 ", d.r("1d20",show_rolls=1,flag_spec=100))
