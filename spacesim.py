import pygame
import pygame_gui

from gameModel import GameModel
from views import (
    MenuContext,
    OrbitContext,
    SurfaceContext,
    ColonyContext,
    TechContext,
    OCMode,
    SCMode,
    GUICode,
)


from pygame.locals import (
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800


def main(testingCallback=None):
    gameModel = GameModel()

    pygame.init()
    manager = pygame_gui.UIManager((1200, 800))
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    guiContext = MenuContext(screen, gameModel, manager)

    clock = pygame.time.Clock()

    running = True
    while running:
        time_delta = clock.tick(60) / 1000.0

        gameModel.tick()

        outerEvent = guiContext.run()

        if outerEvent == QUIT:
            running = False




        elif isinstance(outerEvent, GUICode):
            manager.clear_and_reset()
            if outerEvent == GUICode.LOADORBITVIEW_TARGET_RETURN:
                # Return from surface after setting surface target for ship
                guiContext = OrbitContext(
                    screen,
                    gameModel,
                    manager,
                    mode=OCMode.Target,
                    info = guiContext.info
                )
            elif outerEvent == GUICode.LOADORBITVIEW_LAUNCH_LAND_RETURN:
                guiContext = OrbitContext(
                    screen,
                    gameModel,
                    manager,
                    mode=OCMode.LaunchPlan,
                    info = guiContext.info
                )
            elif outerEvent == GUICode.LOADORBITVIEW_LAUNCH_PLAN and isinstance(
                guiContext, ColonyContext
            ):
                # Launch planning from colony
                guiContext = OrbitContext(
                    screen,
                    gameModel,
                    manager,
                    mode=OCMode.LaunchPlan,
                    info=guiContext.info
                )
            elif outerEvent == GUICode.LOADORBITVIEW_LAUNCH_PLAN and isinstance(
                guiContext, SurfaceContext
            ):
                # Launch planning from surface
                guiContext = OrbitContext(
                    screen,
                    gameModel,
                    manager,
                    mode=OCMode.LaunchPlan,
                    info = guiContext.info
                )
            elif outerEvent == GUICode.LOADORBITVIEW:
                # Direct access
                if hasattr(guiContext, "upperContext") and isinstance(guiContext.upperContext, GameModel):
                    gameModel = guiContext.upperContext
                guiContext = OrbitContext(screen, gameModel, manager)

            elif outerEvent == GUICode.LOADMENUVIEW:
                guiContext = MenuContext(screen, gameModel, manager)

            elif outerEvent == GUICode.LOADTECHVIEW:
                guiContext = TechContext(screen, gameModel, manager)

            elif outerEvent == GUICode.LOADSURFACEVIEW:
                guiContext = SurfaceContext(
                    screen,
                    gameModel,
                    manager,
                    guiContext.upperContext["planet"]
                )


            elif outerEvent == GUICode.LOADSURFACEVIEW_LANDING_PLAN:
                # Drop down to set target for landing
                planet = guiContext.info.end.planet
                guiContext = SurfaceContext(
                    screen,
                    gameModel,
                    manager,
                    planet,
                    mode=SCMode.Landing,
                    info = guiContext.info
                )
            elif outerEvent == GUICode.LOADSURFACEVIEW_LAUNCH_RETURN:
                planet = guiContext.info.start.id
                guiContext = SurfaceContext(
                    screen,
                    gameModel,
                    manager,
                    planet,
                    mode=SCMode.Target,
                    info = guiContext.info
                )

            elif outerEvent == GUICode.LOADCOLONYVIEW:
                if "colony" not in guiContext.upperContext:
                    print("Invalid state - tried to load colony view with no colony")
                    assert False
                colony = gameModel.colonySim.colonyById(
                    guiContext.upperContext["colony"]
                )
                guiContext = ColonyContext(screen, gameModel, manager, colony)
            elif outerEvent == GUICode.LOADCOLONYVIEW_LAUNCH_RETURN:
                # Return to ColonyContext after setting launch target
                guiContext = ColonyContext(
                    screen, gameModel, manager, colony, info = guiContext.info
                )

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.update()

        if testingCallback:
            testingCallback(gameModel, guiContext)

    pygame.quit()


if __name__ == "__main__":
    print("Launching spacesim")
    main()
