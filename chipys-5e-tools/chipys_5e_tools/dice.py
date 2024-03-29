import random as rng
import datetime
import time
import logging

def __init__():
    pass

class RollLog:
    def __init__(self,result:int, formula:str, raw_rolls:str="",datetime_float:float=0, adv:bool=False, bls:bool= False,dis:bool= False,elv:bool= False,ins:bool= False,gwm:bool= False, spe:int=0) -> None:
        self.result = result
        self.time_stamp = datetime_float
        self.formula = formula
        self.adv = adv
        self.bls = bls
        self.dis = dis
        self.elv = elv
        self.ins = ins
        self.gwm = gwm
        self.spe = spe

        if self.time_stamp == 0:
            self.time_stamp = time.time()

class Ledger:
    def __init__(self) -> None:
        self.history = []

    def _last_entry_index(self)-> int:
        """internal Method to return the last entry in the Ledger

        Returns:
            int: returns the index of the last entry
        """
        return len(self.history)-1

    def log(self, new_entry:RollLog):
        """Simple method to add (append) a new entry to the ledger

        Args:
            new_entry (RollLog): accepts RollLog entries for later use
        """
        self.history.append(new_entry)
        print("Logging:", len(self.history) ,new_entry.__dict__)

    def lookup_last(self, number_of_entries:int)->list:
        """Method to fetch and return a list filled with the most recent RollLog objects

        Args:
            number_of_entries (int): The number of desired entries to return

        Returns:
            list: list of RollLog objects (access .result params for dice data)
        """
        l = self._last_entry_index()
        return self.lookup_range(l-number_of_entries,l)

    def lookup_range(self, first_index:int, last_index:int)->list:
        """Method to fetch and return a list filled with RollLog objects

        Args:
            first_index (int): inital index (inclusive)
            last_index (int): ending index (inclusive)

        Returns:
            list: list of RollLog objects (access .result params for dice data)
        """
        requested_list=[]
        for i in range(first_index, last_index):
            v = self.lookup_entry(i)
            if v:
                requested_list.append(v)
        return requested_list
    
    def lookup_entry(self, entry_index:int):
        """Method to recall an entry from the Ledger. 

        Args:
            entry_index (int, optional): The index of the entry that is being request. When missing or set to a value below 0 it will return the most recent entry. Defaults to -1.

        Returns:
            RollLog: Object of the requested Entry (in RollLog format so use ".result" for just the dice roll)
        """
        l = self._last_entry_index()
        #assert 0 <= entry_index <= l  # AKA invalid index will fail

        if 0 <= entry_index <= l:
            return self.history[entry_index]
        else:
            print(f"lookup of index:{entry_index}")
            return False

    def avg_of_last(self, number_of_rolls:int=-1)->float:
        """Method to fetching the last X number of entries and then averages the rolls (uses .avg_of_range(0,X))

        Args:
            number_of_rolls (int, optional): Number of entries to include where any negative value is assumed to be the last entry. Defaults to -1.

        Returns:
            float: Returns a float value that is the AVG rounded to .0
        """
        i = self._last_entry_index()
        if number_of_rolls < 0:
            number_of_rolls=i
        return self.avg_of_range(i - number_of_rolls, i)

    def avg_of_range(self, first_index:int, last_index:int)->float:
        """Method used to fetch and average the rolls from range A-B (both inclusive)

        Args:
            first_index (int): inital index (inclusive)
            last_index (int): ending index (inclusive)

        Returns:
            float: Returns a float value that is the AVG rounded to .0
        """
        lookup_list = []
        for i in range(first_index, last_index):
            lookup_list.append(self.history[i].result)
        return round(sum(lookup_list)/len(lookup_list),1)

    def min_of_last(self, number_of_rolls:int)->int:
        """Alias for min_of_range() for the last X number entries prior to _last_entry_index()

        Args:
            number_of_rolls (int): number of rolls to consider

        Returns:
            int: lowest value rolled in the given history range
        """
        i = self._last_entry_index()
        return self.min_of_range(i-number_of_rolls,i)

    def min_of_range(self, first_index:int, last_index:int)->int:
        """Methhd to fetch range of entries from ledger then return the lowest roll

        Args:
            first_index (int): inital index (inclusive)
            last_index (int): ending index (inclusive)
            
        Returns:
            int: Lowest roll found within the range
        """
        range_list = self.lookup_range(first_index, last_index)
        lowest_roll = 99
        for item in range_list:
            if item.result < lowest_roll:
                lowest_roll = item.result
        return lowest_roll

    def max_of_last(self, number_of_rolls:int)->int:
        """Alias for max_of_range() for the last X number entries prior to _last_entry_index()

        Args:
            number_of_rolls (int): number of rolls to consider

        Returns:
            int: highest value rolled in the given history range
        """
        i = self._last_entry_index()
        return self.max_of_range(i-number_of_rolls,i)

    def max_of_range(self, first_index:int, last_index:int)->int:
        """Methhd to fetch range of entries from ledger then return the highest roll

        Args:
            first_index (int): inital index (inclusive)
            last_index (int): ending index (inclusive)
            
        Returns:
            int: Highest roll found within the range
        """
        range_list = self.lookup_range(first_index, last_index)
        highest_roll = 0
        for item in range_list:
            if item.result > highest_roll:
                highest_roll = item.result
        return highest_roll

class Dice:
    """General dice object to collect and run dice formulas 
    """
    def __init__(self):
        self.ledger = Ledger()

    def roll(self, formula:str="1d20", show_rolls:bool= False, adv:bool=False, bls:bool= False, dis:bool= False, elv:bool= False, ins:bool= False, gwm:bool= False, spe:int=0, log:bool=True) -> int:
        """Public method for rolling a full dice formula allowing for all flagflag_bls needed in DnD5e

        Args:
            formula (str, optional): Desired dice-formula to roll written in the #d##+#d##+# format. EXAMPLE: 1d20+2d4+3. Defaults to "1d20".
            flag_adv (bool, optional): When True the first dice in the formula will get one additional roll and the lower will be dropped. So "2d20" would become 3x d20 rolls with the lowest dropped. Defaults to False.
            show_rolls (bool, optional): When True return value will be an array including each dice roll and the originating formula. Defaults to False.
            flag_bls (bool, optional): _description_. Defaults to False.
            flag_dis (bool, optional): _description_. Defaults to False.
            flag_ela (bool, optional): _description_. Defaults to False.
            flag_ins (bool, optional): _description_. Defaults to False.
            flag_gwm (bool, optional): _description_. Defaults to False.
            flag_spec (int, optional): _description_. Defaults to 0.

        Returns:
            int: final dice value (CAN ALSO return (int,str,str) with show_rolls flag that tells you what dice rolled and what the origin formula was)
        """
        dice_report= ""
        adv_rolled = False
        int_value = 0
        split_formula = formula.split("+")  # | (pipe) separates delimiters
        # Blessed gets handled here ------------- flag_bls
        if bls:
            split_formula.append("1d4")
            
        for element in split_formula:
            if "d" in element:
                # Advantage get handled here ------------- flag_adv
                # Disadvantage get handled here ------------- flag_dis
                # ElvenAccuracy get handled here ------------- flag_ela
                # Inspiration get handled here ------------- flag_ins

                # all of these are only being applied to the first dice in the formula and only once 
                if not adv_rolled:
                    i, s = self._roll_with_adv(element, adv=adv, dis=dis, ins=ins, elv=elv)
                    dice_report += str(s)
                    int_value += i
                    adv_rolled = True
                else:
                    i, s = self._roll_with_adv(element)
                    dice_report += str(s)
                    int_value += i                    
            else:
                int_value += int(element)

        # SharpShooter/GreatWepMaster gets handled here ------------- flag_gwm
        if gwm:
            int_value -= 5

        # SPECIAL gets handled here ------------- flag_gwm
        int_value += spe            
        
        if log:
            self.ledger.log(RollLog(int_value, raw_rolls=dice_report, formula=str(split_formula), adv=adv, bls=bls, dis=dis, elv=elv, ins=ins, gwm=gwm, spe=spe))

        # check what info to return and return it
        if show_rolls:
            return int_value, dice_report, split_formula
        else:
            return int_value
    
    def _roll_with_adv(self, dice_string="1d20", adv:bool=False, dis:bool=False, ins:bool=False, elv:bool=False):
        """Internal Method that handles the portion of rolling a dice value of formula value and adv/dis taking into account

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
        if adv or ins:
            adv_counter +=1
        if dis:
            adv_counter -=1          

        adv_rolled = False
        dice_rolls = []
        kept_rolls = []
        dice_array = dice_string.split("d")
        # loop ones for each dice being roll 
        for i in range(int(dice_array[0])):
            # base dice
            roll = self._roll_single_dice(dice_array[1])
            dice_rolls.append(roll)
            kept_rolls.append(roll)      

            # if we've not yet rolled advantages for this dice formula yet (can't only get one adv)
            # we do this on the first roll so that we can manipulate the list safely
            if not adv_rolled:
                # if there are adv/dis to be applied roll a second dice
                if adv_counter!=0:
                    dice_rolls.append(self._roll_single_dice(dice_array[1]))
                    adv_rolled = True
                    # if we have positive advantage then drop lower of the two
                    if adv_counter>0:
                        
                        # if we have Elven Accuracy we do a 3rd dice and drop lowest
                        if elv:
                            # roll the double adv and keep best
                            dice_rolls.append(self._roll_single_dice(dice_array[1]))
                            dice_rolls.sort()
                            kept_rolls = dice_rolls[2:]
                        else:
                            # sort and keep best per normal adv
                            dice_rolls.sort()
                            kept_rolls = dice_rolls[1:]
                    else:
                        dice_rolls.sort()
                        kept_rolls = dice_rolls[:1]      

        return sum(kept_rolls), dice_rolls

    def _roll_single_dice(self, sides_to_roll=0):
        """Most basic roll command to generate a random number within the range

        Returns:
            int: face value of this roll
        """
        if not sides_to_roll:
            sides_to_roll = self.sides
        return int(rng.randrange(1,int(sides_to_roll)+1))

    def max_roll(self, formula:str="1d20+5")->int:
        """Simple loop to check for the highest possible dice roll of a dice formula

        Args:
            formula (str, optional): Dice formula. Defaults to "1d20+5".

        Returns:
            int: Max possible roll value
        """
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
    print("1d20 ", d.roll("1d20"))
    print("1d20+1 ", d.roll("1d20+1"))
    print("2d20 ", d.roll("2d20"))
    print("2d20 a", d.roll("2d20",True))
    print("2d20 a", d.roll("2d20",True,True))
    print("2d20 a", d.roll("4d20",show_rolls=True, adv=1, elv=1))
    print("1d20 gwm", d.roll("1d20",show_rolls=1,gwm=1))
    print("1d20 ", d.roll("1d20",show_rolls=1,spe=100))
    print("2d20 ", d.roll("2d20",show_rolls=1,adv=True))

    # logging
    print("History: ", d.ledger.avg_of_last())
    print("History: ", d.ledger.avg_of_last(5))
    print("History: ", d.ledger.lookup_range(0,2))
    print("History: ", d.ledger.max_of_last(5))
    print("History: ", d.ledger.min_of_last(5))
    print("History: ", d.ledger.lookup_last(1))
    print("len:",len(d.ledger.history))
