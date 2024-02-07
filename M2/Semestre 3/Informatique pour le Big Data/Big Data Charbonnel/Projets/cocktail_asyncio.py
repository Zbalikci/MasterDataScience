#!/bin/env python3

from projet_cocktail_balikci import Bar, Pic, Barman, Serveur
import sys
import asyncio

if __name__ == "__main__":
    commandes = sys.argv[1:]
    pic = Pic()
    bar = Bar()
    barman = Barman(pic, bar)
    serveur = Serveur(pic, bar, commandes)
    async def main():
        tasks = [serveur.prendre_commande(), asyncio.create_task(barman.preparer()), serveur.servir()]
        await asyncio.gather(*tasks)
    asyncio.run(main())