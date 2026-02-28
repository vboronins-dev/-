import tkinter as tk

root = tk.Tk()
root.title("Clash Royale Map")
root.geometry("900x600")
root.resizable(False, False)

canvas = tk.Canvas(root, width=900, height=600, bg="lightgray")
canvas.pack()


field_x0, field_y0 = 50, 50
field_x1, field_y1 = 850, 550


grass = "#7ec850"
river = "#4aa3df"
bridge = "#8b5a2b"
king = "#a52a2a"
princess = "#d2691e"
road = "#c0c0c0"


canvas.create_rectangle(field_x0, field_y0, field_x1, field_y1,
                        fill=grass, outline="darkgreen", width=2)


river_h = 100
river_y0 = (field_y0 + field_y1) // 2 - river_h // 2
river_y1 = river_y0 + river_h
canvas.create_rectangle(field_x0, river_y0, field_x1, river_y1,
                        fill=river, outline="blue", width=1)


bridge_w = 120

bridge_left_x0 = field_x0 + 150
bridge_left_x1 = bridge_left_x0 + bridge_w
canvas.create_rectangle(bridge_left_x0, river_y0, bridge_left_x1, river_y1,
                        fill=bridge, outline="saddlebrown", width=2)

bridge_right_x0 = field_x1 - 150 - bridge_w
bridge_right_x1 = bridge_right_x0 + bridge_w
canvas.create_rectangle(bridge_right_x0, river_y0, bridge_right_x1, river_y1,
                        fill=bridge, outline="saddlebrown", width=2)


for x in (bridge_left_x0, bridge_left_x1 - 10):
    canvas.create_rectangle(x, field_y0, x + 10, river_y0, fill=road, outline="gray")
    canvas.create_rectangle(x, river_y1, x + 10, field_y1, fill=road, outline="gray")
for x in (bridge_right_x0, bridge_right_x1 - 10):
    canvas.create_rectangle(x, field_y0, x + 10, river_y0, fill=road, outline="gray")
    canvas.create_rectangle(x, river_y1, x + 10, field_y1, fill=road, outline="gray")

king_r = 35
king_x = (field_x0 + field_x1) // 2

canvas.create_oval(king_x - king_r, field_y1 - 80 - king_r,
                   king_x + king_r, field_y1 - 80 + king_r,
                   fill=king, outline="black", width=2)

canvas.create_oval(king_x - king_r, field_y0 + 80 - king_r,
                   king_x + king_r, field_y0 + 80 + king_r,
                   fill=king, outline="black", width=2)


pr_r = 20
positions = [(field_x0 + 80, field_y1 - 80),
             (field_x1 - 80, field_y1 - 80),
             (field_x0 + 80, field_y0 + 80),
             (field_x1 - 80, field_y0 + 80)]
for x, y in positions:
    canvas.create_oval(x - pr_r, y - pr_r, x + pr_r, y + pr_r,
                       fill=princess, outline="black", width=2)


for i in range(8):
    x = field_x0 + 100 + i * 100
    canvas.create_line(x, field_y0, x, field_y1, fill="darkgreen", dash=(2,4))
for i in range(5):
    y = field_y0 + 100 + i * 100
    canvas.create_line(field_x0, y, field_x1, y, fill="darkgreen", dash=(2,4))



root.mainloop()