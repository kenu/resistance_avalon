import asyncio
import discord
import random
from roles import *
from game_room import game_room
from game_info import game_info

mission_result = {
	"success" : 0,
	"fail" : 0
}

mission_message = {}

async def start_mission(team):
	mission_result = {
	"success" : 0,
	"fail" : 0
	}
	mission_message.clear()
	name_team = [member.name for member in team]
	embed = discord.Embed(title="이제 미션을 수행할 차례입니다!", description=f"현재 팀원은 {' '.join(name_team)}입니다.")
	embed.add_field(name="아래 이모티콘을 통해 성공과 실패 중 하나를 골라주세요!", value="성공은 ⭕를, 실패는 ❌를 누르시면 됩니다!")
	for player in team:
		mission_message[player] = await player.send(embed=embed)
		await mission_message[player].add_reaction("⭕")
		if roles[player] in [MORDRED, MORGANA, OBERON, EVIL, ASSASSIN]:
			await mission_message[player].add_reaction("❌")

async def try_mission(payload, team):
	person = None
	for member in game_room['members']:
		if member.id == payload.user_id:
			person = member
	if person:
		if str(payload.emoji) == "⭕":
			mission_result['success'] += 1
			await person.send("미션 성공을 선택하셨습니다.")
		else:
			mission_result["fail"] += 1
			await person.send("미션 실패를 선택하셨습니다.")
		await mission_message[person].delete()
		if mission_result['success'] + mission_result['fail'] == len(team):
			await judge_mission()

async def judge_mission():
	embed = discord.Embed(title=f"원정대의 미션 결과는 다음과 같습니다.")
	if not mission_result['fail'] or (mission_result['fail'] == 1 and len(game_room['members']) >= 7 and game_info['round'] == 4):
		embed.add_field(name="원정대는 무사히 미션을 성공하였습니다!", value=f"성공: {mission_result['success']} 실패: {mission_result['fail']}")
		game_info['round_success'] += 1
	else:
		embed.add_field(name="원정대는 아쉽게도 미션을 실패하였습니다...", value=f"성공: {mission_result['success']} 실패: {mission_result['fail']}")
		game_info['round_fail'] += 1
	await game_room['main_channel'].send(embed=embed)