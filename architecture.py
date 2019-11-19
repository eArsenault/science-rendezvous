

class Cup:

    def __init__(self, i_d, starting_position, session, chosen):

        self.history = [starting_position]
        self.session = session
        self.i_d = i_d
        self.chosen = chosen

        self.past_position = None
        self.past_direction = None

        self.position = starting_position
        self.direction = None

        self.position_pred = None
        self.direction_pred = None


class Session:
    def __init__(self):
        cup_list = []

        self.cup1 = Cup(0,0,self,False)
        self.cup2 = Cup(1,1,self,False)
        self.cup3 = Cup(2,2,self,False)

        cup_list.append(self.cup1)
        cup_list.append(self.cup2)
        cup_list.append(self.cup3)

        self.video_finished = False
        #Setup
        play_area = {
            "leftmost": cup1,
            "middle": cup2,
            "rightmost": cup3
        }

        session_processing()


    def session_processing(self):
        record()
        sequence()
        decide()

    """
     Return video PATH and set chosen cup's chosen property using initial user input
    """
    def record(self):
        pass

    """
     Abstracted main loop to create cup history
    """
    def sequence(self):
        while not self.video_finished:
            frame = next_frame()
            if occlusion(frame):
                result = analyze_occlusion(frame)
                set_new_state(result)

    """
     Change the cup object's properties using the results from the occlusion analysis
    """
    def set_new_state(self):
        pass

    """
     If two discrete colour gradients (seperate cups) turn into one (occlusion), return True:
    """
    def occlusion(self):
        cups_locations = fast_edge_detection()
        if cups_locations["quantity"] < 3:
            return True
        else:
            return False
            # We're good

    """
     Occlusion is happening, rewind a few (3-5) frames and return the following dictionary:
     return = {
        "occluding": <cup_id>
        "occluded": <cup_id>
     }

     Curve algorithm:
     Take the derivative of the curve at the bottom of the mask and find a critical point. 
     If a critical point is found, we know that's where one cup ends and another begins. 
     The occluding cup is the one with a full curve before the occluding cup's curve begins
    """
    def analyze_occlusion(self, frame):

    # Moves on to the next frame, keeping track of the progress of the video
    def next_frame(self):
        pass

    def decide(self):
        pass


if __name__ == "__main__":
    session = Session()