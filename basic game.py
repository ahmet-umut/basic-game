from arcade import open_window as opewin, set_background_color as sebaco, draw_circle_filled as drcifi, Window as windo, schedule as sched, start_render as staren, run as run, draw_line as dralin, key as key
from random import randrange as ranran
import arcade as arcad
from math import sin,cos,pi

colos= [255,255,255*1], [255,0*1,255], [0]*3, [0]*3
for a in range(len(colos)): exec(f"colo{a}=colos[a]")

width=999
heigh=333
title="the game to be reinforced"

class objec:
	def __init__(obje, x,y, radiu=6, colo=colo1, *paras):
		obje.radiu =radiu
		obje.posit = obje.x,obje.y = x,y
		obje.vx,obje.vy = 0,0
		obje.ax,obje.ay = 0,0
		obje.colo =colo
	def draw(obje):
		drcifi(*obje.posit, obje.radiu, obje.colo)
	def updat(obje, dtime):
		obje.x += dtime * (obje.vx+dtime*obje.ax/2)
		obje.y += dtime * (obje.vy+dtime*obje.ay/2)
		obje.updatposit()
		obje.vx += dtime * obje.ax
		obje.vy += dtime * obje.ay
	def updatposit(obje): obje.posit = obje.x,obje.y

class Ball(objec):
	"""docstring for Ball"""
	def __init__(ball,agent, radiu=4, colo=colo3, veloc=0):
		super().__init__(agent.x,agent.y, radiu,colo)
		ball.vx = cos(agent.dire)*veloc
		ball.vy = sin(agent.dire)*veloc
	def updat(ball):
		super().updat(dtime)
		ball.x %= width
		ball.y %= heighb


class Agent(objec):
	"""docstring for Agent"""
	def __init__(agent,game, mass=1, **paras):
		super().__init__(**paras)
		agent.game =game
		agent.mass = mass
		agent.dire,agent.vdire,agent.adire = [0]*3#dire: direction in radiants.
		agent.fthru = 0#thrust force
		agent.thrum = 9#thrusting multiplier: reflects the thrusting power of the agent
	def draw(agent):
		super().draw()
		dralin(*agent.posit, agent.x + cos(agent.dire)*agent.radiu*2, agent.y + sin(agent.dire)*agent.radiu*2, colo2)#draws the directipn line
	def updat(agent, dtime):
		agent.ax = agent.fthru * cos(agent.dire) / agent.mass
		agent.ay = agent.fthru * sin(agent.dire) / agent.mass
		super().updat(dtime)
		agent.dire += dtime * (agent.vdire + dtime*agent.adire/2)
		agent.dire %= pi*2
		agent.vdire += dtime * agent.adire
	def fire(agent):
		agent.game.balls.append(Ball(agent, veloc=99))


class Game(windo):
	def __init__(game,*paras):
		super().__init__(*paras)
		game.fpsco=0#FPS counter
		game.agents = []
		game.balls = []
	def setup(game):
		sebaco(colo0)

		game.aagent(x=111,y=111)
		for a in range(len(game.agents)): exec(f"game.agent{a}=game.agents[a]")

		game.agent0.vx = 6
		
	def aagent(game,**paras):#add agent
		game.agents.append(Agent(game,**paras))
	def on_draw(game):
		staren()
		for b in game.balls: b.draw()
		for a in game.agents: a.draw()
	def on_update(game,dtime):#delta time
		for a in game.agents: a.updat(dtime)
		for b in game.balls: b.updat(dtime)
	def on_key_press(game,ke,modif):
		agent= game.agent0
		match ke:
			case key.ENTER: game.close()
			case key.RIGHT: agent.adire =-1#clockwise
			case key.LEFT: agent.adire =1#anticlockwise
			case key.UP: agent.fthru = agent.thrum	#thrust to the direction
			case key.SPACE: agent.fire()
	def on_key_release(game,ke,modif):
		agent= game.agent0
		match ke:
			case key.RIGHT|key.LEFT: agent.adire =0
			case key.UP: agent.fthru =0

if __name__=="__main__":
	game= Game(width,heigh,title)
	game.setup()
	run()