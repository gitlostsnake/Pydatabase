from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from backend import Database as database
from twilio.rest import Client
from map1 import findmp as mplocator
from jobplotter import advanced_warning_signs as job_plotter_test


"""To do"""
# {OPTIONAL} have the display boxes show a grid or dataframe with column titles
# Start working on the additional data tables
# once additional data has been sorted start adding in a job calculator
# Once calculator is finished add in option to auto complete
# Start making charts for visial representation of the data
# Take the program from tkinter to html css + java
"Find markerpost and put it on a folium map DONE"


def open_map():
    new_window = tk.Toplevel(map)


def road_location():
    mplocator(My_Gui.mp_text.get(), My_Gui.bound_text.get(),
              My_Gui.area_text.get())


def job_plot():
    # lat, lon, len + filename
    lat, lon = My_Gui.coords_text.get().split(',')
    map_name = selected_roadworks[1]
    len = My_Gui.end_inkm_text.get()
    job_plotter_test(lat, lon, len, map_name)


def warning_text(item_name):
    account_sid = ''
    auth_token = ''
    client = Client(account_sid, auth_token)
    message = client.messages \
                .create(
                    body=f'Your running low on {item_name}'),
                    #from='', to='')


class GUI:
    """Tkinter"""

    def __init__(self, master):
        self.master = master
        master.title("TM database")

        class Selected(object):
            """Selected item in the list boxes"""
            @staticmethod
            def job(*args):
                global selected_roadworks
                index = My_Gui.joblistbox.curselection()[0]
                selected_roadworks = My_Gui.joblistbox.get(index)

                My_Gui.location_entry.delete(0, END)
                My_Gui.location_entry.insert(END, selected_roadworks[1])
                My_Gui.client_entry.delete(0, END)
                My_Gui.client_entry.insert(END, selected_roadworks[2])
                My_Gui.startdate_entry.delete(0, END)
                My_Gui.startdate_entry.insert(END, selected_roadworks[3])
                My_Gui.enddate_entry.delete(0, END)
                My_Gui.enddate_entry.insert(END, selected_roadworks[4])
                return selected_roadworks

            @staticmethod
            def additional(*args):
                pass

            @staticmethod
            def stock(*args):
                global selected_item
                index = My_Gui.stocklistbox.curselection()[0]
                selected_item = My_Gui.stocklistbox.get(index)
                id = selected_item[0]
                for row in database.Search.stock(id):
                    My_Gui.stockname_entry.delete(0, END)
                    My_Gui.stockname_entry.insert(END, row[1])
                    My_Gui.stockamount_entry.delete(0, END)
                    My_Gui.stockamount_entry.insert(END, row[2])
                    My_Gui.stockweight_entry.delete(0, END)
                    My_Gui.stockweight_entry.insert(END, row[3])
                    My_Gui.stockwarning_entry.delete(0, END)
                    My_Gui.stockwarning_entry.insert(END, row[4])
                    return selected_item

            @staticmethod
            def vehicle(*args):
                global selected_vehicle
                index = My_Gui.vehiclelistbox.curselection()[0]
                selected_vehicle = My_Gui.vehiclelistbox.get(index)
                My_Gui.fleet_entry.delete(0, END)
                My_Gui.fleet_entry.insert(END, selected_vehicle[1])
                My_Gui.reg_entry.delete(0, END)
                My_Gui.reg_entry.insert(END, selected_vehicle[2])
                My_Gui.weight_entry.delete(0, END)
                My_Gui.weight_entry.insert(END, selected_vehicle[3])
                return selected_vehicle

            @staticmethod
            def assigned_stock(*args):
                global selected_assigned
                index = My_Gui.assignedlistbox.curselection()[0]
                selected_assigned = My_Gui.assignedlistbox.get(index)
                return selected_assigned

        class View(object):
            """View """

            @staticmethod
            def job():
                My_Gui.joblistbox.delete(0, END)
                for row in database.View.job():
                    My_Gui.joblistbox.insert(END, row)

            @staticmethod
            def stock():
                """Stock done shows warning """

                My_Gui.stocklistbox.delete(0, END)
                no_of_assigned = len(database.View.assigned())

                if no_of_assigned <= 0:
                    My_Gui.stocklistbox.delete(0, END)
                    for row in database.View.stock():
                        My_Gui.stocklistbox.insert(END, row)
                else:
                    for row in database.View.stock():
                        id = row[0]
                        i = 0
                        total_amount = int(row[2])
                        amounts = database.Search.assigned_taken(id)
                        if len(amounts) >= 1:
                            numbers = []

                            while i < len(amounts):
                                data = database.Search.assigned_joinitem(id)
                                numbers.append(data[i][3])
                                i += 1

                            total_used = 0
                            for num in numbers:
                                total_used = int(num) + int(total_used)

                            available = int(row[2]) - total_used
                            warning_level = int(row[2]) / int(row[4])

                            if available <= warning_level:

                                current_percent = total_used / int(row[2]) * 100
                                percent_inverter = 100 - int(current_percent)

                                warning_display = [str(id), row[1],
                                                str(available), "/", row[2],
                                                " !>",
                                                str(int(percent_inverter)), "%",
                                                "<!"]

                                My_Gui.stocklistbox.insert(END, " ".join(warning_display))
                                warning_top = [f"{row[1]} Shortage!"]
                                warning_message = [f"""Need more than {int(warning_level)} to continue without triggering a warning. Message sent to manager"""]
                                messagebox.showwarning(warning_top[0], warning_message[0])
                                # The next line is how the program will send texts to users
                                # print("YOU NEED TO ADD IN YOUR OWN DETAILS line 19-20 for texts to work")
                                # warning_text(row[1])

                            else:
                                current_percent = total_used / int(row[2]) * 100
                                percent_inverter = 100 - int(current_percent)

                                info = [str(id), row[1],
                                                str(available), "/", row[2],
                                                " |",
                                                str(int(percent_inverter)), "%",
                                                "| "]

                                My_Gui.stocklistbox.insert(END, " ".join(info))

                        elif len(amounts) == 0:

                            info = [str(id), row[1],
                                            row[2], "/", row[2],
                                            " |",
                                            "100", "%",
                                            "| "]

                            My_Gui.stocklistbox.insert(END, " ".join(info))

                        else:
                            number = amounts[0]
                            available = int(row[2]) - int(number[0])
                            current_percent = int(available) / int(row[2]) * 100
                            info = [str(id), row[1], str(available), "/", row[2],
                                    "|" , str(int(current_percent)), "%", "|"]
                            My_Gui.stocklistbox.insert(END, " ".join(info))

            @staticmethod
            def vehicle():
                My_Gui.vehiclelistbox.delete(0, END)
                for row in database.View.vehicle():
                    My_Gui.vehiclelistbox.insert(END, row)

            @staticmethod
            def assigned():
                My_Gui.assignedlistbox.delete(0, END)
                for row in database.View.assigned():
                    My_Gui.assignedlistbox.insert(END, row)

        class Search(object):
            """Search bar and viewing specific data from assigned tables"""

            @staticmethod
            def job():
                pass
            "Used to find out whats in the kitlist of a job"
            @staticmethod
            def assigned():
                My_Gui.assignedlistbox.delete(0, END)
                for row in database.Search.assigned_kitlist(selected_roadworks[0]):
                    My_Gui.assignedlistbox.insert(END, row[5] + " " + row[3])

        class Delete(object):
            """Delete job, stock or vehicle."""

            @staticmethod
            def job():
                database.Delete.job(Selected.job()[0])
                My_Gui.joblistbox.delete(0, END)
                for row in database.View.job():
                    My_Gui.joblistbox.insert(END, row)

            @staticmethod
            def stock():
                database.Delete.stock(Selected.stock()[0])
                My_Gui.stocklistbox.delete(0, END)
                View.stock()

            @staticmethod
            def vehicle():
                database.Delete.vehicle(Selected.vehicle()[0])
                My_Gui.vehiclelistbox.delete(0, END)
                for row in database.View.vehicle():
                    My_Gui.vehiclelistbox.insert(END, row)

            @staticmethod
            def assigned():
                database.Delete.assigned(Selected.job()[0])
                My_Gui.assignedlistbox.delete(0, END)
                for row in database.View.assigned():
                    My_Gui.assignedlistbox.insert(END, row)

        class InsertEntry(object):

            @staticmethod
            def job():
                database.Insert.job(My_Gui.location_text.get(), My_Gui.client_text.get(),
                                   My_Gui.startdate_text.get(), My_Gui.enddate_text.get())
                My_Gui.joblistbox.delete(0, END)
                for row in database.View.job():
                    My_Gui.joblistbox.insert(END, row)

            @staticmethod
            def stock():
                database.Insert.stock(My_Gui.stockname_text.get(), My_Gui.stockamount_text.get(),
                                     My_Gui.stockweight_text.get(), My_Gui.stockwarning_text.get())
                My_Gui.stocklistbox.delete(0, END)
                View.stock()

            @staticmethod
            def vehicle():
                database.Insert.vehicle(My_Gui.fleet_text.get(), My_Gui.reg_text.get(),
                                       My_Gui.weight_text.get())
                My_Gui.vehiclelistbox.delete(0, END)
                for row in database.View.vehicle():
                    My_Gui.vehiclelistbox.insert(END, row)

            @staticmethod
            def additional():
                database.Insert.additional(selected_roadworks[0], My_Gui.joblength_text.get(),
                                    My_Gui.jobtype_text.get(), My_Gui.crewrequired_text.get(),
                                    My_Gui.shift_type_text.get())
                print(database.View.additional())

        class Update(object):

            @staticmethod
            def job():
                database.Update.job(selected_roadworks[0], My_Gui.location_text.get(),
                                   My_Gui.client_text.get(), My_Gui.startdate_text.get(),
                                   My_Gui.enddate_text.get())
                My_Gui.joblistbox.delete(0, END)
                for row in database.View.job():
                    My_Gui.joblistbox.insert(END, row)

            @staticmethod
            def stock():
                database.Update.stock(selected_item[0], My_Gui.stockname_text.get(),
                                     My_Gui.stockamount_text.get(), My_Gui.stockweight_text.get(),
                                     My_Gui.stockwarning_text.get())
                My_Gui.stocklistbox.delete(0, END)
                for row in database.View.stock():
                    My_Gui.stocklistbox.insert(END, row)

        class Assign(object):

            @staticmethod
            def stock():
                amount_taken = simpledialog.askstring("Input Required", "Please input the amount needed")
                database.Insert.assigned(selected_item[0], selected_roadworks[0], amount_taken)
                My_Gui.assignedlistbox.delete(0, END)
                for row in database.View.assigned():
                    My_Gui.assignedlistbox.insert(END, row)
                View.stock()

            @staticmethod
            def vehicle():
                pass

            @staticmethod
            def person():
                pass

        """Main Job buttons"""
        self.view_job = Button(window, text="View Job", width=12,
                               command=View.job)
        self.view_job.grid(row=1, column=0)

        self.delete_job = Button(window, text="Delete Job", width=12,
                                 command=Delete.job)
        self.delete_job.grid(row=2, column=0)

        self.assign_stock = Button(window, text="Assign Stock", width=12,
                                   command=Assign.stock)
        self.assign_stock.grid(row=3, column=0)

        """UNDER CONSTRUCTION"""
        self.assign_vehicle = Button(window, text="Assign vehicle", width=12)
        self.assign_vehicle.grid(row=4, column=0)
        """TO-DO"""

        self.print_out = Button(window, text="Print Out", width=12)
        self.print_out.grid(row=5, column=0)

        self.view_kitlist = Button(window, text="View KitList", width=12,
                                   command=Search.assigned)
        self.view_kitlist.grid(row=6, column=0)

        self.delete_assigned = Button(window, text="Delete KitList", width=12,
                                      command=Delete.assigned)
        self.delete_assigned.grid(row=7, column=0)

        self.view_assigned = Button(window, text="View assigned stock", width=12,
                                    command=View.assigned)
        self.view_assigned.grid(row=8, column=0)

        self.insert_job = Button(window, text="Create Job", width=12,
                                 command=InsertEntry.job)
        self.insert_job.grid(row=17, column=4)

        self.update_job = Button(window, text="Update Job", width=12,
                                 command=Update.job)
        self.update_job.grid(row=18, column=4)

        """Main Stock buttons"""
        self.view_stock = Button(window, text="View Stock", width=12,
                                 command=View.stock)
        self.view_stock.grid(row=25, column=0)

        self.remove_stock = Button(window, text="Remove Stock", width=12,
                                   command=Delete.stock)
        self.remove_stock.grid(row=29, column=0)


        """Main Vehicle buttons"""
        self.view_vehicle = Button(window, text="View Vehicle", width=12,
                                   command=View.vehicle)
        self.view_vehicle.grid(row=41, column=0)

        self.create_vehicle = Button(window, text="Add Vehicle", width=12,
                                     command=InsertEntry.vehicle)
        self.create_vehicle.grid(row=45, column=19)

        self.remove_vehicle = Button(window, text="Del Vehicle", width=12,
                                     command=Delete.vehicle)
        self.remove_vehicle.grid(row=43, column=0)

        """List boxes"""
        """Job"""
        self.joblistbox = Listbox(window, height=12, width=70)
        self.joblistbox.grid(row=1, column=1, rowspan=15, columnspan=15)

        self.job_scrollbar = Scrollbar(window)
        self.job_scrollbar.configure(command=self.joblistbox.yview)

        self.joblistbox.configure(yscrollcommand=self.job_scrollbar.set)
        self.joblistbox.bind('<<ListboxSelect>>', Selected.job)

        """Assigned"""
        self.assigned_label = Label(window, text="Assigned Stock")
        self.assigned_label.grid(row=0, column=18)

        self.assignedlistbox = Listbox(window, height=12, width=30)
        self.assignedlistbox.grid(row=1, column=18, rowspan=15, columnspan=7)

        self.assignedlistbox.bind('<<ListboxSelect>>', Selected.assigned_stock)

        """Stock"""
        self.stock_label = Label(window, text="")
        self.stock_label.grid(row=22, column=2)

        self.stocklistbox = Listbox(window, height=5, width=70)
        self.stocklistbox.grid(row=23, column=1, rowspan=15, columnspan=15)

        self.spacer_label = Label(window, text="")
        self.spacer_label.grid(row=40, column=0)

        self.stock_scrollbar = Scrollbar(window)
        self.stocklistbox.configure(yscrollcommand=self.stock_scrollbar.set)
        self.stock_scrollbar.configure(command=self.stocklistbox.yview)

        self.stocklistbox.bind('<<ListboxSelect>>', Selected.stock)

        """Vehicles"""
        self.vehiclelistbox = Listbox(window, height=5, width=70)
        self.vehiclelistbox.grid(row=41, column=1, rowspan=15, columnspan=15)

        self.vehiclelistbox.bind('<<ListboxSelect>>', Selected.vehicle)

        """Entry Mid section"""
        """Job Entry Fields"""

        self.location_label = Label(window, text="Location")
        self.location_label.grid(row=17, column=0)
        self.location_text = StringVar()
        self.location_entry = Entry(window, textvariable=self.location_text)
        self.location_entry.grid(row=17, column=1)

        self.client_label = Label(window, text="Client")
        self.client_label.grid(row=18, column=0)
        self.client_text = StringVar()
        self.client_entry = Entry(window, textvariable=self.client_text)
        self.client_entry.grid(row=18, column=1)

        self.startdate_label = Label(window, text="Start Date \nYYYY-MM-DD 00:00")
        self.startdate_label.grid(row=17, column=2)
        self.startdate_text = StringVar()
        self.startdate_entry = Entry(window, textvariable=self.startdate_text)
        self.startdate_entry.grid(row=17, column=3)

        self.enddate_label = Label(window, text="End Date \nYYYY-MM-DD 00:00")
        self.enddate_label.grid(row=18, column=2)
        self.enddate_text = StringVar()
        self.enddate_entry = Entry(window, textvariable=self.enddate_text)
        self.enddate_entry.grid(row=18, column=3)

        """Stock Entry Fields"""

        self.stockname_label = Label(window, text="Stock name")
        self.stockname_label.grid(row=20, column=0)
        self.stockname_text = StringVar()
        self.stockname_entry = Entry(window, textvariable=self.stockname_text)
        self.stockname_entry.grid(row=20, column=1)

        self.stockamount_label = Label(window, text="Amount")
        self.stockamount_label.grid(row=21, column=0)
        self.stockamount_text = StringVar()
        self.stockamount_entry = Entry(window, textvariable=self.stockamount_text)
        self.stockamount_entry.grid(row=21, column=1)

        self.stockweight_label = Label(window, text="Weight kg")
        self.stockweight_label.grid(row=20, column=2)
        self.stockweight_text = StringVar()
        self.stockweight_entry = Entry(window, textvariable=self.stockweight_text)
        self.stockweight_entry.grid(row=20, column=3)

        self.stockwarning_label = Label(window, text="Warning %")
        self.stockwarning_label.grid(row=21, column=2)
        self.stockwarning_text = StringVar()
        self.stockwarning_entry = Entry(window, textvariable=self.stockwarning_text)
        self.stockwarning_entry.grid(row=21, column=3)

        """Stock Entry buttons"""

        self.create_stock = Button(window, text="Create Stock", width=12,
                                   command=InsertEntry.stock)
        self.create_stock.grid(row=20, column=4)

        self.update_stock = Button(window, text="Update Stock", width=12,
                                   command=Update.stock)
        self.update_stock.grid(row=21, column=4)

        """Additional Entry section"""

        self.additional_label = Label(window, text="Additional \nData")
        self.additional_label.grid(row=16, column=19)

        self.joblength_label = Label(window, text="km")
        self.joblength_label.grid(row=17, column=18)
        self.joblength_text = StringVar()
        self.joblength_entry = Entry(window, textvariable=self.joblength_text)
        self.joblength_entry.grid(row=17, column=19)

        self.additional_types_label = Label(window, text="Type")
        self.additional_types_label.grid(row=18, column=18)
        self.additional_types = {'Temporary', 'Static', 'Traffic Control', 'Other'}
        self.jobtype_text = StringVar()
        self.jobtype_text.set('Temporary')
        self.jobtype_dropdown = OptionMenu(window, self.jobtype_text,
                                           *self.additional_types)
        self.jobtype_dropdown.grid(row=18, column=19)

        self.crewrequired_label = Label(window, text="Crew Size")
        self.crewrequired_label.grid(row=19, column=18)
        self.crewrequired_text = StringVar()
        self.crewrequired_entry = Entry(window, textvariable=self.crewrequired_text)
        self.crewrequired_entry.grid(row=19, column=19)

        self.additional_shift_label = Label(window, text="Shift")
        self.additional_shift_label.grid(row=20, column=18)
        self.additional_shift = {'Day 6am-6pm', 'Night 6pm-6am', 'Day + Night'}
        self.shift_type_text = StringVar()
        self.shift_type_text.set('Day 6am-6pm')
        self.shift_type_dropdown = OptionMenu(window, self.shift_type_text,
                                           *self.additional_shift)
        self.shift_type_dropdown.grid(row=20, column=19)

        self.update_additional = Button(window, text="Update Additional",
                                        width=16, command=InsertEntry.additional)
        self.update_additional.grid(row=21, column=19)

        """Vehicle Entry section"""

        self.fleet_label = Label(window, text='fleet no')
        self.fleet_label.grid(row=41, column=18)
        self.fleet_text = StringVar()
        self.fleet_entry = Entry(window, textvariable=self.fleet_text)
        self.fleet_entry.grid(row=41, column=19)

        self.reg_label = Label(window, text='reg')
        self.reg_label.grid(row=42, column=18)
        self.reg_text = StringVar()
        self.reg_entry = Entry(window, textvariable=self.reg_text)
        self.reg_entry.grid(row=42, column=19)

        self.weight_label = Label(window, text='weight limit')
        self.weight_label.grid(row=43, column=18)
        self.weight_text = StringVar()
        self.weight_entry = Entry(window, textvariable=self.weight_text)
        self.weight_entry.grid(row=43, column=19)

        """Location """

        self.mp_label = Label(window, text='Search Marker Post')
        self.mp_label.grid(row=1, column=25)
        self.mp_text = StringVar()
        self.mp_entry = Entry(window, textvariable=self.mp_text)
        self.mp_entry.grid(row=1, column=26)

        self.bound_label = Label(window, text='AL / TL')
        self.bound_label.grid(row=2, column=25)
        self.bound_options = {'North bound', 'South bound'}
        self.bound_text = StringVar()
        self.bound_dropdown = OptionMenu(window, self.bound_text,
                                        *self.bound_options)
        self.bound_dropdown.grid(row=2, column=26)

        self.area_label = Label(window, text='Area')
        self.area_label.grid(row=3, column=25)
        self.area_options = ['AREA1', 'AREA2', 'AREA3', 'AREA4', 'AREA5', 'AREA6',
                             'AREA7', 'AREA8', 'AREA9', 'AREA10', 'AREA11', 'AREA12',
                             'AREA13', 'AREA14']
        self.area_text = StringVar()
        self.area_dropdown = OptionMenu(window, self.area_text,
                                        *self.area_options)
        self.area_dropdown.grid(row=3, column=26)

        self.findmp_button = Button(window, text="Search",
                                    command=road_location)
        self.findmp_button.grid(row=4, column=26)

        """Job plotter section"""

        self.job_plot_label = Label(window, text='plot a job')
        self.job_plot_label.grid(row=6, column=25)
        self.job_coords_label = Label(window, text='using coordinates for')
        self.job_coords_label.grid(row=6, column=26)
        self.job_using_label = Label(window, text='taper location')
        self.job_using_label.grid(row=7, column=25)

        self.coords_text = StringVar()
        self.coords_entry = Entry(window, textvariable= self.coords_text)
        self.coords_entry.grid(row=7, column=26)
        self.end_inkm_label = Label(window, text='length in km')
        self.end_inkm_label.grid(row=8, column=25)
        self.end_inkm_text = StringVar()
        self.end_inkm_entry = Entry(window, textvariable=self.end_inkm_text)
        self.end_inkm_entry.grid(row=8, column=26)

        self.plot_button = Button(window, text='Add to map',
                                            command=job_plot)
        self.plot_button.grid(row=9, column=26)

        """Add custom marker onto map"""
        self.edit_map_label = Label(window, text='Edit map')
        self.edit_map_label.grid(row=16, column=25)

        self.custom_markers = ['Splitter', 'Merge', 'push', 'rejoin', 'other']
        self.markers_text  = StringVar()
        self.markers_dropdown = OptionMenu(window, self.markers_text,
                                            *self.custom_markers)
        self.markers_dropdown.grid(row=17, column=26)

        self.custom_mp_text = StringVar()
        self.custom_mp_entry = Entry(window, text=self.custom_mp_text)
        self.custom_mp_entry.grid(row=18,column=26)
        self.custom_mp_label = Label(window, text='location mp')
        self.custom_mp_label.grid(row=18, column=25)

        self.open_map_button = Button(window, text='Open Map', command=open_map)
        self.open_map_button.grid(row=19, column=26)


window = Tk()
My_Gui = GUI(window)
window.mainloop()
