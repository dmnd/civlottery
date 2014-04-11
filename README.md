civlottery
==========

Assigns random civs to players, but allows players to veto initial assignments.

See the testgame directory for example input. Vetoes should be listed in the order they are received.

Nerdy details
-------------

Note that the scheme does not require players to trust the player who executes
the script. This is likely completely unnecessary, but was fun to design
anyway.

It works by allowing (but not requiring) each player to contribute a seed. All
seeds are combined to seed the random number generator. So that players don't
have to trust the executor, the executor should generate their seed before any other player does, and publicise a hash of this seed.

Once final assignments have been generated, the executor can prove the results
were not tampered with by publishing all seeds. Any other player should then be
able to reproduce the assignments, verifying that they are fair.
