
    def __next__(self):
        if self.n == self.len:
            raise StopIteration
        else:
            temp = self.data[self.n]
            self.n += 1
            return temp