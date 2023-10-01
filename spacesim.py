import pygame
import pygame_gui

from gameModel import GameModel
from views.menuContext import MenuContext
from views.orbitContext import OrbitContext
from views.surfaceContext import SurfaceContext
from views.colonyContext import ColonyContext


from pygame.locals import (
    QUIT,
)

from views.orbitContext import OCMode
from views.surfaceContext import SCMode

from views.guiContext import GUICode


# Define constants for the screen width and height
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800


def main(testingCallback=None):
    pygame.init()

    manager = pygame_gui.UIManager((1200, 800))

    guiContext = None
    gameModel = GameModel()

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
                landingContext = {
                    "ship": guiContext.upperContext["ship"],
                    "target": guiContext.upperContext["node"],
                    "surfaceCoordinates": guiContext.upperContext["surfaceCoordinates"],
                }
                guiContext = OrbitContext(
                    screen,
                    gameModel,
                    manager,
                    mode=OCMode.Target,
                    landingContext=landingContext,
                )
            elif outerEvent == GUICode.LOADORBITVIEW_LAUNCH_LAND_RETURN:
                landingContext = guiContext.upperContext
                guiContext = OrbitContext(
                    screen,
                    gameModel,
                    manager,
                    mode=OCMode.LaunchPlan,
                    landingContext=landingContext,
                )
            elif outerEvent == GUICode.LOADORBITVIEW_LAUNCH_PLAN and isinstance(
                guiContext, ColonyContext
            ):
                # Launch planning from colony
                landingContext = {
                    "ship": guiContext.upperContext["ship"],
                    "colony": guiContext.upperContext["colony"],
                }
                guiContext = OrbitContext(
                    screen,
                    gameModel,
                    manager,
                    mode=OCMode.LaunchPlan,
                    landingContext=landingContext,
                )
            elif outerEvent == GUICode.LOADORBITVIEW_LAUNCH_PLAN and isinstance(
                guiContext, SurfaceContext
            ):
                # Launch planning from surface
                landingContext = guiContext.upperContext
                guiContext = OrbitContext(
                    screen,
                    gameModel,
                    manager,
                    mode=OCMode.LaunchPlan,
                    landingContext=landingContext,
                )
            elif outerEvent == GUICode.LOADORBITVIEW:
                # Direct access
                guiContext = OrbitContext(screen, gameModel, manager)

            elif outerEvent == GUICode.LOADMENUVIEW:
                guiContext = MenuContext(screen, gameModel, manager)

            elif outerEvent == GUICode.LOADSURFACEVIEW:
                planet = gameModel.planetSim.planetById(
                    guiContext.upperContext["planet"]
                )
                guiContext = SurfaceContext(screen, gameModel, manager, planet)
            elif outerEvent == GUICode.LOADSURFACEVIEW_LANDING_PLAN:
                # Drop down to set target for landing
                landingContext = {
                    "ship": guiContext.upperContext["ship"],
                    "targetPlanet": guiContext.upperContext["targetPlanet"],
                    "node": guiContext.upperContext["node"],
                    "trajectory": guiContext.upperContext["trajectory"],
                }
                if "colony" in guiContext.upperContext:
                    landingContext["colony"] = guiContext.upperContext["colony"]
                elif "planet" in guiContext.upperContext:
                    landingContext["planet"] = guiContext.upperContext["planet"]

                planet = gameModel.planetSim.planetById(
                    guiContext.upperContext["targetPlanet"]
                )
                guiContext = SurfaceContext(
                    screen,
                    gameModel,
                    manager,
                    planet,
                    mode=SCMode.Landing,
                    landingContext=landingContext,
                )
                # Return from setting launch target for confirmation
            elif outerEvent == GUICode.LOADSURFACEVIEW_LAUNCH_RETURN:
                planet = gameModel.planetSim.planetById(
                    guiContext.upperContext["planet"]
                )
                landingContext = {
                    "ship": guiContext.upperContext["ship"],
                    "planet": guiContext.upperContext["planet"],
                    "trajectory": guiContext.upperContext["trajectory"],
                }
                if "targetPlanet" in guiContext.upperContext:
                    landingContext["targetPlanet"] = guiContext.upperContext[
                        "targetPlanet"
                    ]
                guiContext = SurfaceContext(
                    screen,
                    gameModel,
                    manager,
                    planet,
                    mode=SCMode.Target,
                    landingContext=landingContext,
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
                launchContext = {
                    "ship": guiContext.upperContext["ship"],
                    "trajectory": guiContext.upperContext["trajectory"],
                }
                colony = gameModel.colonySim.colonyById(
                    guiContext.upperContext["colony"]
                )
                guiContext = ColonyContext(
                    screen, gameModel, manager, colony, launchContext=launchContext
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
