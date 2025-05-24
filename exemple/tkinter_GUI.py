""" Ce fichier fait la liaison entre tout les scripts 
et les incluent dans une interface Tkinter
"""
import tkinter as tk
from tkinter import ttk

from matplotlib_GUI import GameOfLifePLT
from history import History
from algo_game_of_life import AlgoGameOfLife
from menu_game_of_life import Menu_GameOfLife


class GameOfLifeTk(GameOfLifePLT):
    def __init__(self, json_data, callback_grid_sound, callback_button_sound):
        self.callback_grid_sound = callback_grid_sound
        self.callback_button_sound = callback_button_sound
        
        self.root = tk.Tk()
        self.root.config(bg="White")
        self.root.geometry("800x850")
        # self.root.iconbitmap("./music/Glider.ico")
        self.root.title("Game of Life")
        super().__init__(json_data,callback = self.on_clic_callback,update = self.next_gen)
        
        self.menu_game_of_life = Menu_GameOfLife(self.root)
        #self.barre_menu.pack()
        
        self.game_of_life = AlgoGameOfLife(json_data)
        
        self.tkinter_integration(self.root)
        
        #    ------------    Button   ------------
        self.button_frame = tk.Frame(self.root,background="White")
        self.button_frame.pack(side='bottom')
        
        # Apparence des boutons
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, background="white")
        
        # Créer et placer les boutons
        self.previous_button = ttk.Button(self.button_frame, text="Previous", takefocus=False, command=self.previous)
        self.previous_button.pack(side="right", padx=10, pady=10, ipady=5)
        
        self.next_gen_button = ttk.Button(self.button_frame, text="Next", takefocus=False, command=lambda : self.next_gen(song=True))
        self.next_gen_button.pack(side="left", padx=10, pady=10, ipady=5)
        
        self.start_button = ttk.Button(self.button_frame, text="Start", takefocus=False, command=self.launch_animation)
        self.start_button.pack(side="right", padx=10, pady=10, ipady=5)
        
        self.clear_button = ttk.Button(self.button_frame, text="Clear", takefocus=False, command=self.clear)
        self.clear_button.pack(side="right", padx=10, pady=10, ipady=5)
        
        self.random_button = ttk.Button(self.button_frame, text="Random", takefocus=False, command=self.random_fill)
        self.random_button.pack(side="right", padx=10, pady=10, ipady=5)
        
        
        self.history = History(json_data)
        
        life = self.game_of_life.reload_life()
        self.update_grid_from_array(life)
        
        self.first = True
        
        self.root.mainloop()
    
    
    
    def clear(self):
        """Réinitialise la grille et le ndarray"""
        self.callback_button_sound()
        self.clear_grid()
        self.game_of_life.clear_cell()
    
    
    def next_gen(self,*arg,song=False):
        """Ca permet de passer à la generation suivantes"""
        if song:
            self.callback_button_sound()
        next = self.game_of_life.generation_manager()
        self.clear_grid()
        self.update_grid_from_array(next)
        self.history.history_append(next)
    
    
    def random_fill(self):
        """Remplit la grilles avec certaines cellules aux hasard"""
        self.callback_button_sound()
        life = self.game_of_life.random_fill()
        self.update_grid_from_array(life)
        
    
    
    def previous (self):
        """Ca permet de passer à la generation précédente"""
        self.callback_button_sound()
        previous = self.history.time_travel()
        self.update_grid_from_array(previous)
        self.game_of_life.cell_status = previous.copy()
    
    
    
    def on_clic_callback(self,i,j):
        """Récupère l'info de clic venant de la class matplotlib et la renvoie vers la class algo"""
        self.game_of_life.on_clic_set_game_of_life_algo(i,j)
        try: 
            self.callback_grid_sound()
        except:
            print(" No Noise !!!!!!!")
    
    def launch_animation(self):
        """Cette fonction lance l'animation"""
        self.callback_button_sound()
        if self.first:
            self.start_button.config(text = "Stop")
            # Je sais pas pk mais l'animation ne se lance pas direct
            self.anim = self.animation_()
            # mais l'animation se lance correctement après cet appel
            self.next_gen(song=True)
            self.first = False
        else:
            self.start_button.config(text = "Start")
            self.anim.event_source.stop()
            self.first = True



if __name__ == "__main__":
    from json_controler import get_constant_and_limit
    json_data = get_constant_and_limit()
    def noise():
        """il n'y a pas de son a jouer !!"""
        pass
    g = GameOfLifeTk(json_data,noise,noise)