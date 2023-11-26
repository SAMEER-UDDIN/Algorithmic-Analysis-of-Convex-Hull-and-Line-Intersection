import tkinter as tk

class LineSegment:
    def __init__(self, start, end):
        self.start = start
        self.end = end

class GeometricAlgorithmApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Line Segment Intersection")

        self.canvas = tk.Canvas(self.master, width=500, height=500)
        self.canvas.pack()

        self.segments = []
        self.start_point = None

        self.canvas.bind("<ButtonPress-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw_segment)
        self.canvas.bind("<ButtonRelease-1>", self.end_drawing)
        self.canvas.bind("<Button-3>", self.detect_intersections)

    def start_drawing(self, event):
        self.start_point = (event.x, event.y)

    def draw_segment(self, event):
        current_point = (event.x, event.y)
        self.canvas.delete("temp_line")  # Remove previous temporary lines
        self.canvas.create_line(self.start_point[0], self.start_point[1],
                                current_point[0], current_point[1], fill="black", tags="temp_line")

    def end_drawing(self, event):
        end_point = (event.x, event.y)
        self.segments.append(LineSegment(self.start_point, end_point))
        self.canvas.create_line(self.start_point[0], self.start_point[1],
                                end_point[0], end_point[1], fill="black")

    def detect_intersections(self, event):
        if len(self.segments) >= 2:
            for i in range(0, len(self.segments) - 1, 2):
                seg1 = self.segments[i]
                seg2 = self.segments[i + 1]
                if self.intersect_segments(seg1, seg2):
                    self.canvas.create_text(250, 250, text="Intersecting!", fill="red", font=("Helvetica", 16))
                    break
            else:
                self.canvas.create_text(250, 250, text="Not Intersecting", fill="green", font=("Helvetica", 16))

# #Parametric Equation Method
#     @staticmethod
#     def intersect_segments(seg1,seg2):
#         x1, y1 = seg1.start
#         x2, y2 = seg1.end
#         x3, y3 = seg2.start
#         x4, y4 = seg2.end
#
#         def on_segment(p, q, r):
#             return (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]))
#
#         def parametric_equation(p, q, t):
#             return ((1 - t) * p[0] + t * q[0], (1 - t) * p[1] + t * q[1])
#
#         def do_intersect(p1, q1, p2, q2):
#             for t1 in [0, 1]:
#                 for t2 in [0, 1]:
#                     point1 = parametric_equation(p1, q1, t1)
#                     point2 = parametric_equation(p2, q2, t2)
#                     if point1 == point2 or on_segment(p1, point2, q1) or on_segment(p2, point1, q2):
#                         return True # Intersecting
#
#             return False # Not intersecting
#
#         return do_intersect((x1, y1), (x2, y2), (x3, y3), (x4, y4))

# Cross Product Method
    @staticmethod
    def intersect_segments(seg1, seg2):
        x1, y1 = seg1.start
        x2, y2 = seg1.end
        x3, y3 = seg2.start
        x4, y4 = seg2.end

        def orientation(p, q, r):
            val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
            if val == 0:
                return 0  # Collinear
            return 1 if val > 0 else 2  # Clockwise or counterclockwise

        def on_segment(p, q, r):
            return (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
                    q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]))

        o1 = orientation((x1, y1), (x2, y2), (x3, y3))
        o2 = orientation((x1, y1), (x2, y2), (x4, y4))
        o3 = orientation((x3, y3), (x4, y4), (x1, y1))
        o4 = orientation((x3, y3), (x4, y4), (x2, y2))

        if o1 != o2 and o3 != o4:
            return True  # Intersecting
        if (o1 == 0 and on_segment((x1, y1), (x3, y3), (x2, y2))) or \
                (o2 == 0 and on_segment((x1, y1), (x4, y4), (x2, y2))) or \
                (o3 == 0 and on_segment((x3, y3), (x1, y1), (x4, y4))) or \
                (o4 == 0 and on_segment((x3, y3), (x2, y2), (x4, y4))):
            return True  # Intersecting
        return False  # Not intersecting

if __name__ == "__main__":
    root = tk.Tk()
    app = GeometricAlgorithmApp(root)
    root.mainloop()
