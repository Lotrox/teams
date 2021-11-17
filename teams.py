#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Daniel Martinez
# Description: API REST Framework Bottle. Tutorial Sencillo.

from bottle import Bottle, route, run, request, HTTPResponse, response, hook
import json


import random
import re

# Disparador encargado de habilitar el acceso a origenes distintos en todas las llamadas.
@hook('after_request')
def enable_cors():
        response.headers['Access-Control-Allow-Origin']  =  '*'    
        response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


# Soporte para llamadas CORS con peticion OPTIONS.
@route('/', method = 'OPTIONS')
@route('/<path:path>', method = 'OPTIONS')
def options_handler(path = None):
    return {}


# {"Dani": 12, "Angel": 40, "Luismi": 20, "Pablo": 10, "Mochuelo": 60, "Manuel": 35, "Pabol": 40, "Aceituno": 10, "Fernando": 40, "Milla": 12}

@route('/teams/<nmax>', method='POST')
def teams(nmax=3):	
	elo = request.body.read()
	print elo
	jelo = json.loads(elo)
	jelo = eval(json.dumps(jelo))
	print jelo
	players = []
	total  = []
	listTeams = []
	# jelo = {}

	# ELO to JSON
	for player in jelo:
		players.append(player)
	
	while True:
		random.shuffle(players)
		teamA = [5]
		teamA[0] = players[0]

		for i in players:
			if len(teamA) >= 5:
				teamA.sort()
				if not teamA in total:
					total.append(teamA)
				break
			if not i in teamA:
				teamA.append(i)

		pointTeamA = 0
		for i in teamA:
			pointTeamA += int(jelo[i])
		pointTeamA = pointTeamA/5.0
		teamB = list(set(players) - set(teamA))
		teamB.sort()
		pointTeamB = 0
		for i in teamB:
				pointTeamB += int(jelo[i])
		pointTeamB = pointTeamB/5.0

		if not teamB in total:
			total.append(teamB)
			pointDiff = abs(pointTeamA - pointTeamB)
			team = {}
			team['pointDiff'] = pointDiff
			team['teamA'] = teamA
			team['pointA'] = pointTeamA
			team['teamB'] = teamB
			team['pointB'] = pointTeamB
			# listTeams.append(str(pointDiff) + " <br>" + str(teamA) + "<br> (" + str(pointTeamA) + ") VS (" + str(pointTeamB) + ") <br>" + str(teamB) + "<br><br>")
			listTeams.append(team)
		# Numero total maximo de combinaciones
		if len(total) >= 252:
			break


	listTeams.sort(key=lambda s: s['pointDiff'])

	# listTeams.reverse()
	# for i in listTeams:
	# 	print i
	print json.dumps(listTeams[0:int(nmax)])
	raise HTTPResponse(body=json.dumps(listTeams[0:int(nmax)]), status=200)



run(host='0.0.0.0', port=8080, reloader=True)




