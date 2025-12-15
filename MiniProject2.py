import tkinter as tk
from tkinter import ttk
import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

g= 9.81 # m/s²


def analytically( H, vx, vy, vz ):
  # z(t)= H + vz t - g/2 t² = 0    ballistic trajectory
  #       c   bt     at²           a,b,c for Mitternachtsformel
  a= -g / 2.0
  b= vz
  c= H
  wurzelterm= b * b - 4 * a * c
  t1= ( -b + np.sqrt( wurzelterm ) ) / ( 2 * a )
  t2= ( -b - np.sqrt( wurzelterm ) ) / ( 2 * a )
  t= max( t1, t2 )                 # choose longer trajectory

  T= np.linspace( 0, t, 300 )      # 300t values
  X= T * vx                        # constant motion in
  Y= T * vy                        # relation to the floor
  Z= H + T * vz - T*T * g / 2.0    # ballistic trajectory

  return X, Y, Z


class BallSimulator:

  def __init__( self, root ):
    self.root= root

    control= ttk.Frame( root, padding=10 )
    control.pack( side=tk.LEFT, fill=tk.Y )

    ttk.Label( control, text='H [m]').grid(row=0, column=0 )
    ttk.Label( control, text='vx [m/s]').grid(row=1, column=0 )
    ttk.Label( control, text='vy [m/s]').grid(row=2, column=0 )
    ttk.Label( control, text='vz [m/s]').grid(row=3, column=0 )

    self.eH= ttk.Entry( control ); self.eH.grid( row=0, column=1 )
    self.eX= ttk.Entry( control ); self.eX.grid( row=1, column=1 )
    self.eY= ttk.Entry( control ); self.eY.grid( row=2, column=1 )
    self.eZ= ttk.Entry( control ); self.eZ.grid( row=3, column=1 )

    self.eH.insert( 0, '10' )
    self.eX.insert( 0, '1' )
    self.eY.insert( 0, '1' )
    self.eZ.insert( 0, '10' )

    ttk.Button(control, text='Calculate', command=self.run).grid(
      row=4, column=0, columnspan=2, pady=10
    )

    self.info= ttk.Label( control, text='' )
    self.info.grid( row=5, column=0, columnspan=2 )

    fig= Figure( figsize=(6, 5) )
    self.ax = fig.add_subplot( 111, projection='3d' )
    self.ax.set_xlabel( 'x' )
    self.ax.set_ylabel( 'y' )
    self.ax.set_zlabel( 'z' )

    self.line, = self.ax.plot([], [], [], lw=2)
    self.point, = self.ax.plot([], [], [], 'ro')

    self.canvas= FigureCanvasTkAgg( fig, master=root )
    self.canvas.get_tk_widget().pack( side=tk.RIGHT, fill=tk.BOTH, expand=True )

    self.ani = None


  def run( self ):
    try:
        H=  float( self.eH.get() )
        vx= float( self.eX.get() )
        vy= float( self.eY.get() )
        vz= float( self.eZ.get() )
    except ValueError:
        self.info.config( text='invalid input' )
        return

    X, Y, Z= analytically( H, vx, vy, vz )

    self.ax.cla()
    self.ax.set_xlabel( 'x' )
    self.ax.set_ylabel( 'y' )
    self.ax.set_zlabel( 'z' )

    self.ax.plot( X, Y, Z, alpha=0.3 )
    self.ax.scatter( X[-1], Y[-1], Z[-1], color='green', s=50 )

    self.line,  = self.ax.plot( [], [], [], linewidth=2 )
    self.point, = self.ax.plot( [], [], [], color='red', marker='o' )

    self.info.config(
      text= f'landing point: {X[-1]:.2f}/{Y[-1]:.2f}/{Z[-1]:.2f} m'
    )


    def update( i ):
        self.line.set_data( X[:i], Y[:i] )
        self.line.set_3d_properties( Z[:i] )
        self.point.set_data( [X[i]], [Y[i]] )
        self.point.set_3d_properties( [Z[i]] )
        return self.line, self.point

    frames= list( range( 0, len(X), 10 ) )
    if frames[-1] != len(X)-1:
      frames.append( len(X)-1 )

    self.ani= FuncAnimation(
      self.canvas.figure,
      update,
      frames=frames,
      interval=10,
      blit=True,
      repeat=False
    )

    self.canvas.draw()


root= tk.Tk()
root.title( 'MiniProject 2, simple version' )
BallSimulator( root )
root.mainloop()

