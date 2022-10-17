class FoundationObject:
    def __init__(self, length=0, width=0, depth=0, radius=0):
        """
        A foundation class to store the geometric properties of your foundation

        Parameters:
        -----------
        long : int
            Long side of foundation same as length of foundation
        short : int
            Short side of foundation, same as l
        depth : int
        radius : int
        shape : str
            Shape of foundation object
        """
        if length and radius or width and radius:
            raise ValueError('You cannot have length or width with radius')

        if (length and not width) or (width and not length):
            raise ValueError("You cannot have width without length, or viceversa")

        self.long = max(length, width)
        self.short = min(length, width)
        self.depth = depth
        self.radius = radius
        self.shape = self.get_shape()  # You call functions inside the class as methods \
        # Remember that a function defined inside a class is a method,
        # so use it  :)!

    def __repr__(self):
        """
        A foundation representation when you call the ojbect
        """
        if self.radius:
            return f'Foundation: \n Radius:{self.radius} \n Depth:{self.depth}m  \n Shape:{self.shape} '
        else:
            #return f'Foundation: \n Length:{self.long}m \n Width:{self.short}m\n Depth:{self.depth}m\n Shape: {self.shape}'
            return f'Foundation:  Length:{self.long}m  Width:{self.short}m Depth:{self.depth}m Shape: {self.shape}'
    def get_shape(self):
        """
        Cycles through the foundation attributes to check
        which type of foundation it represents.

        """
        if self.radius:
            self.shape = "circular"
        else:
            if self.short >= 10:
                self.shape = "raft"
            else:
                if (self.long / self.short) > 10:
                    self.shape = "strip"
                else:
                    self.shape = "square"
        return self.shape
    # TODO: Implement setter & getter to avoid overwriting of obj.attributes
    # avoid fd.shape = 'raft' -> fd.shape = 'raft' instead of what is defined