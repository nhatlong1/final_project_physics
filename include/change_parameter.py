import tkinter as tk


Material1 = [1.0, "Air"]
Material2 = [1.52, "Glass"]

def show_entry_fields():
	arr = []
	num1 = str(e1.get())
	num2 = str(e2.get())
	arr.append(num1)
	arr.append(num2)
	parameter_value = 'include/parameter_value.txt'
	with open(parameter_value, 'w') as t:
		t.write(arr[0] + ' ')
		t.write(arr[1])



def inputBox():
	global e1,e2
	master = tk.Tk()
	tk.Label(master, text="N1").grid(row=0)
	         
	tk.Label(master, text="N2").grid(row=1)
	         

	e1 = tk.Entry(master)
	e2 = tk.Entry(master)

	e1.grid(row=0, column=1)
	e2.grid(row=1, column=1)


	tk.Button(master,text='Quit',command=master.quit).grid(row=3,column=0, sticky=tk.W,pady=4) 
                                    
                                    
	tk.Button(master, text='Enter', command=show_entry_fields).grid(row=3,column=1,sticky=tk.W, pady=4)
	tk.mainloop()
	# num1 = e1.get()
	# num2 = e2.get()
	# return num1,num2