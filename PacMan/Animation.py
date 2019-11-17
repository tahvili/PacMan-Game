class Animation:

    def __init__(self, anim_type):
        self.anim_type = anim_type
        self.frames = []
        self.point = 0
        self.forward = True
        self.speed = 0
        self.dt = 0

    def add_frame(self, frame):
        self.frames.append(frame)

    def get_frame(self, dt):

        if self.anim_type == "loop":
            self.loop(dt)
        elif self.anim_type == "once":
            self.move_once(dt)
        elif self.anim_type == "ping":
            self.reverse_ping(dt)
        elif self.anim_type == "static":
            self.point = 0
        return self.frames[self.point]

    def next_frame(self, dt):
        self.dt += dt
        if self.dt >= (1.0 / self.speed):
            if self.forward:
                self.point += 1
            else:
                self.point -= 1
            self.dt = 0

    def loop(self, dt):
        """
        When we want an animation to loop we'll use this method
        """

        self.next_frame(dt)
        if self.forward:
            if self.point == len(self.frames):
                self.point = 0
        else:
            if self.point == -1:
                self.point = len(self.frames) - 1

    def move_once(self, dt):
        """
        This type of animation only goes through the list once, then stops.
        """
        self.next_frame(dt)
        if self.forward:
            if self.point == len(self.frames):
                self.point = len(self.frames) - 1
        else:
            if self.point == -1:
                self.point = 0

    def reverse_ping(self, dt):
        """
        This is a different type of looping animation, except when we reach the
        end of the animation we reverse the animation so it goes backwards.
        When it reaches the start of the animation again then we set it to go forward again
        """
        self.next_frame(dt)
        if self.point == len(self.frames):
            self.forward = False
            self.point -= 2
        elif self.point < 0:
            self.forward = True
            self.point = 1
