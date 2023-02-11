import random as rng

def __init__():
    pass

class Dice:
    """General dice object to collect and run dice formulas 
    """
    def __init__(self):
        pass

    def r(self, in_str:str="1d20", advantage:bool=False, show_rolls:bool= False, flag_adv:bool= False, flag_bls:bool= False,flag_dis:bool= False,flag_ela:bool= False,flag_ins:bool= False,flag_pam:bool= False):
        """"alias for self.formula()"""
        return self.formula(in_str, advantage, show_rolls, flag_adv, flag_bls, flag_dis, flag_ela, flag_ins, flag_pam)

    def f(self, in_str:str="1d20", advantage:bool=False, show_rolls:bool= False, flag_adv:bool= False, flag_bls:bool= False,flag_dis:bool= False,flag_ela:bool= False,flag_ins:bool= False,flag_pam:bool= False):
        """"alias for self.formula()"""
        return self.formula(in_str, advantage, show_rolls, flag_adv, flag_bls, flag_dis, flag_ela, flag_ins, flag_pam)

    def formula(self, in_str:str="1d20", advantage:bool=False, show_rolls:bool= False, flag_adv:bool= False, flag_bls:bool= False,flag_dis:bool= False,flag_ela:bool= False,flag_ins:bool= False,flag_pam:bool= False):
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
        for element in formula:
            if "d" in element:
                if advantage and not adv_rolled:
                    i, s = self.roll(element, advantage=True)
                    dice_report += str(s)
                    int_value += i
                    adv_rolled = True
                else:
                    i, s = self.roll(element)
                    dice_report += str(s)
                    int_value += i                    
            else:
                int_value += int(element)
        if show_rolls:
            return int_value, dice_report, in_str
        else:
            return int_value
    
    def roll(self, dice_string="1d20", advantage=False ):
        """Rolls Dice of #d## format string

        Args:
            dice_string (String): A dice roll string in the #d## format
            advantage (Bool): A toggle indicating if there should be advantage (it'll roll one extra dice and drop lowest)

        Returns:
            int: value the dice rolled 
        """
        # int_value=0
        adv_rolled = False
        dice_rolls = []
        dice_array = dice_string.split("d")
        for i in range(int(dice_array[0])):
            if advantage and not adv_rolled:
                dice_rolls.append(self._roll_value(dice_array[1]))
                adv_rolled = True
            dice_rolls.append(self._roll_value(dice_array[1]))        
        if advantage:
            dice_rolls.sort()
            lowest_roll_dropped = dice_rolls[1:]
            return sum(lowest_roll_dropped), dice_rolls
        else:
            return sum(dice_rolls), dice_rolls

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
    print("2d20 a", *d.r("2d20+2",True,True))
