from game.war import PlaneWar


def main():
    """ game entrance, main function """
    war = PlaneWar()
    # 添加敌方小型飞机
    war.add_small_enemies(6)
    war.run_game()


if __name__ == '__main__':
    main()
