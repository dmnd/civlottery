#!/usr/bin/env python


import collections
import hashlib
import os
import random
import sys


def player_seed(player):
    file = "seeds/{}.txt".format(player)
    if not os.path.isfile(file):
        # no seed provided (player trusts everyone) so use name as seed
        return player

    with open(file) as f:
        return f.read().strip()


def assign_civs(civs, players, vetoes, seed):
    rand = random.Random()
    rand.seed(seed)

    shuffled_civs = list(civs)
    rand.shuffle(shuffled_civs)

    # initial assignment
    assignments = collections.defaultdict(list)
    for p, c in zip(players, shuffled_civs):
        assignments[p].append(c)

    # now process vetoes
    remaining_civs = set(shuffled_civs[len(players):])
    for v in vetoes:
        # determine which civs remain eligible for this player
        eligible_civs = remaining_civs - set(assignments[v])

        newciv = rand.choice(sorted(eligible_civs))
        assignments[v].append(newciv)

        # add the previously picked civ back into the pool
        remaining_civs.add(assignments[v][-2])

        # remove the new civ from the pool
        remaining_civs.remove(newciv)

    return assignments


def print_heading(s):
    print s
    print len(s) * '-'


def print_assignments(assignments, players, vetoes):
    print_heading("initial draw")
    for p in players:
        print "{} drew {}".format(p, assignments[p][0])
    print

    print_heading("vetoes")
    veto_index = collections.defaultdict(int)
    for vetoing_player in vetoes:
        assignment_chain = assignments[vetoing_player]
        index = veto_index[vetoing_player]

        oldciv, newciv = assignment_chain[index:index+2]
        veto_index[vetoing_player] += 1

        print "{} vetoed {} and drew {}".format(vetoing_player, oldciv, newciv)
    print

    print_heading("current draw")
    for p in players:
        print "{} is playing as {}".format(p, assignments[p][-1])


def print_seeds(seeds, players):
    print_heading("player: sha256(seed)")
    for p, s in zip(players, seeds):
        print "{}: {}".format(p, hashlib.sha256(s).hexdigest())


def main(gamedir):
    # all civ names, one per line
    civs = sorted(l.strip() for l in open("civs.txt"))

    # names of each player
    players = sorted(
        l.strip() for l in open(os.path.join(gamedir, "players.txt")))

    # vetoes, in order of receipt
    vetoes = [l.strip() for l in open(os.path.join(gamedir, "vetoes.txt"))]

    # seed rng
    seeds = [player_seed(p) for p in players]
    final_seed = "".join(seeds)

    assignments = assign_civs(civs, players, vetoes, final_seed)
    print_assignments(assignments, players, vetoes)
    print
    print_seeds(seeds, players)


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        gamedir = sys.argv[1]
    else:
        gamedir = "testgame"
    main(gamedir)
