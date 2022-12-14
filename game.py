from arcade import open_window as opewin, set_background_color as sebaco, draw_circle_filled as drcifi, Window as windo, schedule as sched, start_render as staren, run as run, draw_line as dralin, key as key
from random import randrange as ranran, random as rando
import arcade as arcad
from math import sin,cos,pi

colos= [255,255,255*1], [0]*3, [0]*3, [0]*3, [111]*3, [111]*3
agentcolos= [255,0*1,255], [222]*3                                                              
for a in range(len(colos)): exec(f"colo{a}=colos[a]")
for a in range(len(agentcolos)): exec(f"agentcolo{a}=agentcolos[a]")
def blcolos(colo1,colo2):#blend colors
	return [(col1+col2)//2 for col1,col2 in zip(colo1,colo2)]

width=999
heigh=333
title="the game to be reinforced"

class objec:
	def __init__(obje, x,y, radiu=6, colo=colo4, *paras):
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
	def __init__(ball,agent, radiu=4, colo=colo2, veloc=0):
		#maybe a lifetime thing can be added
		super().__init__(agent.x,agent.y, radiu,colo)
		ball.vx = cos(agent.dire)*veloc
		ball.vy = sin(agent.dire)*veloc
		ball.agent = agent
		ball.tbdeletd =False#to be deleted
	def updat(ball,dtime):
		super().updat(dtime)
		if ball.tbdeletd or ball.x %width != ball.x or  ball.y %heigh != ball.y:
			ball.agent.game.balls.remove(ball)
			del(ball)
	def delet(ball): ball.tbdeletd =True#delete


class Agent(objec):
	"""docstring for Agent"""
	agentct=0#agent count
	def __init__(agent,game, mass=9,dire=0, **paras):
		super().__init__(**paras)
		agent.colo = agentcolos[Agent.agentct]
		Agent.agentct += 1
		agent.damag =0
		agent.score =0
		agent.game =game
		agent.mass =mass
		agent.dire =dire
		agent.vdire,agent.adire = [0]*2#dire: direction in radiants.
		agent.fthru = 0#thrust force
		agent.thrum = 99#thrusting multiplier: reflects the thrusting power of the agent
	def draw(agent):
		super().draw()
		dralin(*agent.posit, agent.x + cos(agent.dire)*agent.radiu*2, agent.y + sin(agent.dire)*agent.radiu*2, colo3)#draws the directipn line
	def updat(agent, dtime):
		agent.ax = agent.fthru * cos(agent.dire) / agent.mass
		agent.ay = agent.fthru * sin(agent.dire) / agent.mass
		super().updat(dtime)
		agent.dire += dtime * (agent.vdire + dtime*agent.adire/2)
		agent.dire %= pi*2
		agent.vdire += dtime * agent.adire
		agent.x %= width
		agent.y %= heigh
	def fire(agent):
		agent.game.balls.append(Ball(agent, veloc=99, colo= blcolos(agent.colo,colo5)))

# M??GHT ADD FR??CT??ON

class Game(windo):
	def __init__(game,*paras):
		super().__init__(*paras)
		game.fpsco=0#FPS counter
		game.agents = []
		game.balls = []
	def setup(game):
		# sched(game.comfps,4)		#for computing FPS every 4 sec.s
		sebaco(colo0)

		game.aagent(x=ranran(111,888),y=ranran(111,222), dire=rando()*2*pi)
		game.aagent(x=ranran(111,888),y=ranran(111,222), dire=rando()*2*pi)
		for a in range(len(game.agents)): exec(f"game.agent{a}=game.agents[a]")

		
	def aagent(game,**paras):#add agent
		game.agents.append(Agent(game,**paras))
	def comfps(game,dtime):#compute fps
		print(f"FPS: {round(game.fpsco/dtime)}")
		game.fpsco =0
	def on_draw(game):
		staren()
		for b in game.balls: b.draw()
		for a in game.agents: a.draw()
	def on_update(game,dtime):#delta time
		game.fpsco +=1
		for a in game.agents:
			a.updat(dtime)
			for b in game.balls:#collision check
				if b.agent!=a and abs(b.x-a.x) < b.radiu+a.radiu and abs(b.y-a.y) < a.radiu+b.radiu and ((b.x-a.x)**2+(b.y-a.y)**2)**.5<a.radiu+b.radiu:
					a.damag +=1#it may depend on b in next versions
					b.agent.score +=1
					b.delet()#b may not be deleted
		for b in game.balls: b.updat(dtime)

	def on_key_press(game,ke,modif):
		agent0= game.agent0
		agent1= game.agent1
		match ke:
			case key.ENTER: game.close()
			case key.RIGHT: agent0.adire =-1#clockwise
			case key.LEFT: agent0.adire =1#anticlockwise
			case key.UP: agent0.fthru = agent0.thrum	#thrust to the direction
			case key.D: agent1.adire =-1#clockwise
			case key.A: agent1.adire =1#anticlockwise
			case key.W: agent1.fthru = agent1.thrum	#thrust to the direction
			case key.RCTRL: agent0.fire()
			case key.SPACE: agent1.fire()
	def on_key_release(game,ke,modif):
		agent0= game.agent0
		agent1= game.agent1
		match ke:
			case key.RIGHT|key.LEFT: agent0.adire =0
			case key.UP: agent0.fthru =0
			case key.D|key.A: agent1.adire =0
			case key.W: agent1.fthru =0

if __name__=="__main__":
	game= Game(width,heigh,title)
	game.setup()
	run()