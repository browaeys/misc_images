"""Phase d'un mouvement circulaire uniforme et projection sur l'axe x."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from matplotlib.path import Path as PlotPath

plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':15,
                     'mathtext.fontset':'dejavusans', 'svg.fonttype':'none'})
blue = '#28618A'
projection_color = '#C020A0'
phi, theta = np.deg2rad(20), np.deg2rad(68)
p0=np.array([np.cos(phi),np.sin(phi)])
p=np.array([np.cos(theta),np.sin(theta)])
fig,ax=plt.subplots(figsize=(10,8.6))
ax.set_aspect('equal')
ax.set(xlim=(-1.42,1.57),ylim=(-1.19,1.48))
ax.axis('off')
q=np.linspace(0,2*np.pi,600)
ax.plot(np.cos(q),np.sin(q),color='#A4ADB6',lw=1.7,zorder=1)
for end,start in [((1.42,0),(-1.28,0)),((0,1.35),(0,-1.12))]:
    ax.annotate('',end,start,arrowprops=dict(arrowstyle='->',lw=1.35,color='#41464B'))
# Rayon initial et position initiale.
ax.plot([0,p0[0]],[0,p0[1]],ls=(0,(5,4)),lw=1.6,color=blue)
ax.plot(*p0,'o',mfc='white',mec=blue,mew=2,ms=8,zorder=5)
# Rayon courant.
ax.plot([0,p[0]],[0,p[1]],lw=2.2,color=blue,zorder=3)
ax.plot(*p,'o',color=blue,ms=10,zorder=6)
# Arcs avec flèches, en sens trigonométrique.
def angular_arrow(radius,a,b,color,lw=2):
    angles=np.linspace(a,b,120)
    path = PlotPath(np.column_stack((radius*np.cos(angles), radius*np.sin(angles))))
    ax.add_patch(FancyArrowPatch(path=path, arrowstyle='->', mutation_scale=15,
                                lw=lw, color=color, zorder=4))
angular_arrow(.74,0,phi,blue,1.8)
ax.text(.88*np.cos(phi/2),.88*np.sin(phi/2),r'$\varphi$',color=blue,fontsize=19,ha='center',va='center')
angular_arrow(.74,phi,theta,blue)
mid=(phi+theta)/2
ax.text(.88*np.cos(mid),.88*np.sin(mid),r'$\omega t$',color=blue,fontsize=19,ha='center',va='center')
# Vitesse angulaire : flèche extérieure, à partir de la direction du point courant.
angular_arrow(1.2,theta,np.deg2rad(87),blue,2.3)
# Projection orthogonale sur l'axe des abscisses.
ax.plot([p[0],p[0]],[0,p[1]],ls=':',color=projection_color,lw=1.6,zorder=2)
ax.plot(p[0],0,'o',color=projection_color,ms=6,zorder=6)
ax.plot([0,p[0]],[0,0],color=projection_color,lw=3.2,zorder=5)
s=.05
ax.plot([p[0],p[0]-s,p[0]-s],[s,s,0],color=projection_color,lw=1)
ax.annotate(r'$\cos(\omega t+\varphi)$',xy=(p[0]/2,0),xytext=(.51,-.25),
            ha='center',va='center',fontsize=20,color=projection_color,
            arrowprops=dict(arrowstyle='-',color=projection_color,lw=1.2,connectionstyle='angle,angleA=0,angleB=-90,rad=5'))
out=Path(__file__).resolve().parent
for ext in ('png','svg','pdf'):
    fig.savefig(out/f'phase_cercle.{ext}',dpi=220,bbox_inches='tight',facecolor='white',pad_inches=.16)
print(out/'phase_cercle.png')
