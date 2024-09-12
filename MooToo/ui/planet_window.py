""" Display Planet Details"""

import time
from enum import Enum, StrEnum, auto
from typing import Optional, TYPE_CHECKING

import pygame
from MooToo.constants import PopulationJobs, PlanetClimate, PlanetSize, PlanetCategory, MAX_ORBITS
from MooToo.ui.proxy.planet_proxy import PlanetProxy as Planet
from .base_graphics import BaseGraphics, load_image
from .textbox_window import TextBoxWindow
from .constants import DisplayMode
from .gui_button import Button
from .building_choice_window import BuildingChoiceWindow
from ..utils import PlanetId, SystemId

if TYPE_CHECKING:
    from MooToo.ui.game import Game


#####################################################################################################
class PlanetButtons(StrEnum):
    RETURN = auto()
    BUILD = auto()


#####################################################################################################
class ImageNames(Enum):
    FOOD_1 = auto()
    FOOD_X = auto()
    HUNGER_1 = auto()
    HUNGER_X = auto()
    WORK_1 = auto()
    WORK_X = auto()
    POLLUTION_1 = auto()
    POLLUTION_X = auto()
    SCIENCE_1 = auto()
    SCIENCE_X = auto()
    IGNORANCE_1 = auto()
    IGNORANCE_X = auto()
    MONEY_1 = auto()
    MONEY_X = auto()
    DEBT_1 = auto()
    DEBT_X = auto()
    HAPPY = auto()

    FARMER = auto()
    WORKER = auto()
    SCIENTIST = auto()

    WINDOW = auto()
    RETURN_BUTTON = auto()
    BUILD_BUTTON = auto()
    ORBIT_ARROW = auto()


#####################################################################################################
#####################################################################################################
class PlanetWindow(BaseGraphics):
    def __init__(self, screen: pygame.Surface, game: "Game"):
        """ """
        super().__init__(game)
        self.screen = screen
        self.planet_id: Optional[PlanetId] = None
        self.images = load_images()
        self.planet_rects: dict[Planet, pygame.Rect] = {}
        self.worker_rects: dict[tuple[PopulationJobs, int], pygame.Rect] = {}
        self.worker: Optional[tuple[PopulationJobs, int]] = None
        self.detail_rect: Optional[pygame.Rect] = None
        self.colony_font = pygame.font.SysFont("Ariel", 18, bold=True)
        self.display_mode = DisplayMode.PLANET
        self.building_choice_window = BuildingChoiceWindow(screen, game)
        self.buttons = {
            PlanetButtons.RETURN: Button(self.images[ImageNames.RETURN_BUTTON], pygame.Vector2(555, 460)),
            PlanetButtons.BUILD: Button(self.images[ImageNames.BUILD_BUTTON], pygame.Vector2(525, 123)),
        }
        self.details_textbox = TextBoxWindow(screen, game)

    #####################################################################################################
    def details_text(self) -> list[str]:
        planet = self.game.galaxy.planets[self.planet_id]
        empire = self.game.galaxy.empires[planet.owner]
        pop_str = f"{planet.current_population()}/{planet.max_population()}"
        return [
            f"{planet.name} - {empire.name} Colony",
            f"{planet.size} {planet.climate}",
            f"Mineral {planet.richness}",
            f"{planet.gravity} G",
            "",
            f"{'Base food per':<20}{planet.food_per:>30}",
            f"{'Base industry per':<20}{planet.work_per:>30}",
            f"{'Base research per':<20}{planet.science_per:>30}",
            "",
            f"{'Morale':<20}{planet.morale()*10:>29}%",
            "",
            f"{'Population':<20}{pop_str:>30}",
        ]

    #####################################################################################################
    def draw(self) -> None:
        planet = self.game.galaxy.planets[self.planet_id]
        self.draw_centered_image(self.images[planet.climate_image])
        if self.display_mode == DisplayMode.PLANET_BUILD:
            self.building_choice_window.draw()
            return
        if self.display_mode == DisplayMode.PLANET_DETAILS:
            self.details_textbox.draw(self.details_text(), self.title_font)
            return

        self.window = self.draw_centered_image(self.images[ImageNames.WINDOW])
        self.draw_orbits(planet.system_id)
        self.draw_resources(self.planet_id)
        self.draw_pop_label(self.planet_id)
        self.draw_population(self.planet_id)
        self.draw_currently_building(self.planet_id)
        self.draw_government(self.planet_id)
        self.draw_morale(self.planet_id)
        self.draw_buildings(self.planet_id)
        for button in self.buttons.values():
            button.draw(self.screen)
        label_surface = self.colony_font.render(f"{planet.name}", True, "white")
        self.screen.blit(
            label_surface,
            pygame.Rect(
                self.mid_point[0] - label_surface.get_size()[0] / 2,
                0,
                label_surface.get_size()[0],
                label_surface.get_size()[1],
            ),
        )

    #####################################################################################################
    def draw_buildings(self, planet_id: PlanetId) -> None:
        """Draw the current buildings on the planet"""
        top_left = pygame.Vector2(8, 170)
        planet = self.game.galaxy.planets[planet_id]
        for building in planet.buildings:
            text = self.text_font.render(planet[building].name, True, "purple")
            self.screen.blit(text, top_left)
            top_left.y += text.get_size()[1]

    #####################################################################################################
    def draw_morale(self, planet_id: PlanetId) -> None:
        top_left = pygame.Vector2(340, 31)
        planet = self.game.galaxy.planets[planet_id]
        if not planet.owner:
            return
        for _ in range(planet.morale()):
            pos = self.screen.blit(self.images[ImageNames.HAPPY], top_left)
            top_left.x += pos.width

    #####################################################################################################
    def draw_government(self, planet_id: PlanetId) -> None:
        top_left = pygame.Vector2(309, 31)
        planet = self.game.galaxy.planets[planet_id]
        if not planet.owner:
            return
        empire = self.game.galaxy.empires[planet.owner]
        government = empire.government
        image = self.images[f"government_{government}"]
        self.screen.blit(image, top_left)

    #####################################################################################################
    def draw_currently_building(self, planet_id: PlanetId) -> None:
        planet = self.game.galaxy.planets[planet_id]
        if not planet.build_queue:
            return
        center = pygame.Vector2(580, 33)
        building = planet.build_queue[0]
        text_surface = self.label_font.render(building.name, True, "purple")
        self.screen.blit(text_surface, center - pygame.Vector2(text_surface.get_size()[0] / 2, 0))
        if turns := planet.turns_to_build():
            text_surface = self.label_font.render(f"{turns:,} turn(s)", True, "white", "black")
            bottom_right = pygame.Vector2(626, 108)
            top_left = bottom_right - pygame.Vector2(text_surface.get_size()[0], text_surface.get_size()[1])
            self.screen.blit(text_surface, top_left)

    #####################################################################################################
    def draw_population(self, planet_id: PlanetId) -> None:
        """Draw farmers etc"""
        dest = pygame.Vector2(309, 62)
        planet = self.game.galaxy.planets[planet_id]
        rects = self.draw_population_sequence(
            dest, self.images[ImageNames.FARMER], planet.jobs[PopulationJobs.FARMERS], 200
        )
        for num, rect in enumerate(rects):
            self.worker_rects[(PopulationJobs.FARMERS, planet.jobs[PopulationJobs.FARMERS] - num)] = rect

        dest = pygame.Vector2(309, 92)
        rects = self.draw_population_sequence(
            dest, self.images[ImageNames.WORKER], planet.jobs[PopulationJobs.WORKERS], 200
        )
        for num, rect in enumerate(rects):
            self.worker_rects[(PopulationJobs.WORKERS, planet.jobs[PopulationJobs.WORKERS] - num)] = rect

        dest = pygame.Vector2(309, 122)
        rects = self.draw_population_sequence(
            dest, self.images[ImageNames.SCIENTIST], planet.jobs[PopulationJobs.SCIENTISTS], 200
        )
        for num, rect in enumerate(rects):
            self.worker_rects[(PopulationJobs.SCIENTISTS, planet.jobs[PopulationJobs.SCIENTISTS] - num)] = rect

    #####################################################################################################
    def draw_resources(self, planet_id: PlanetId) -> None:
        """Draw the income, food, etc."""
        self.draw_income(planet_id)
        self.draw_food(planet_id)
        self.draw_work(planet_id)
        self.draw_science(planet_id)

    #####################################################################################################
    def draw_income(self, planet_id: PlanetId) -> None:
        planet = self.game.galaxy.planets[planet_id]
        income = planet.money_production
        cost = planet.money_cost
        dest = pygame.Vector2(126, 31)

        dest = self.draw_resource_sequence(
            dest,
            self.images[ImageNames.MONEY_1],
            self.images[ImageNames.MONEY_X],
            income,
        )
        dest.x += 10
        self.draw_resource_sequence(
            dest,
            self.images[ImageNames.DEBT_1],
            self.images[ImageNames.DEBT_X],
            cost,
        )

    #####################################################################################################
    def draw_food(self, planet_id: PlanetId) -> None:
        # Eating Surplus
        planet = self.game.galaxy.planets[planet_id]
        eating = planet.food_cost
        surplus = planet.food_surplus
        dest = pygame.Vector2(126, 60)
        dest = self.draw_resource_sequence(dest, self.images[ImageNames.FOOD_1], self.images[ImageNames.FOOD_X], eating)
        dest.x += 10
        if surplus > 0:
            self.draw_resource_sequence(dest, self.images[ImageNames.FOOD_1], self.images[ImageNames.FOOD_X], surplus)
        else:
            self.draw_resource_sequence(
                dest, self.images[ImageNames.HUNGER_1], self.images[ImageNames.HUNGER_X], -surplus
            )

    #####################################################################################################
    def draw_work(self, planet_id: PlanetId) -> None:
        # Surplus Pollution
        planet = self.game.galaxy.planets[planet_id]
        work = planet.work_surplus
        pollution = planet.work_cost
        dest = pygame.Vector2(126, 90)
        dest = self.draw_resource_sequence(dest, self.images[ImageNames.WORK_1], self.images[ImageNames.WORK_X], work)
        self.draw_resource_sequence(
            dest,
            self.images[ImageNames.POLLUTION_1],
            self.images[ImageNames.POLLUTION_X],
            pollution,
        )

    #####################################################################################################
    def draw_science(self, planet_id: PlanetId) -> None:
        planet = self.game.galaxy.planets[planet_id]
        labs = planet.science_production
        dest = pygame.Vector2(126, 120)
        self.draw_resource_sequence(
            dest,
            self.images[ImageNames.SCIENCE_1],
            self.images[ImageNames.SCIENCE_X],
            labs,
        )

    #####################################################################################################
    def draw_resource_sequence(
        self, top_left: pygame.Vector2, image_1: pygame.Surface, image_x: pygame.Surface, value: int
    ) -> pygame.Vector2:
        """Display a sequence of resource images"""

        for _ in range(value // 10):
            self.screen.blit(image_x, top_left)
            top_left.x += image_x.get_size()[0]
        for _ in range(value % 10):
            self.screen.blit(image_1, top_left)
            top_left.x += image_1.get_size()[0]
        self.debug_text(value, top_left)

        return top_left

    #####################################################################################################
    def draw_pop_label(self, planet_id: PlanetId) -> None:
        planet = self.game.galaxy.planets[planet_id]
        text = f"Pop {int(planet.raw_population / 1000):,}k (+{int(planet.population_increment() / 1000):,}k)"
        text_surface = self.label_font.render(text, True, "white")
        text_size = text_surface.get_size()
        self.screen.blit(text_surface, pygame.Rect(640 - text_size[0], 0, text_size[0], text_size[1]))

    #####################################################################################################
    def draw_orbits(self, system_id: SystemId):
        """Draw the system summary"""
        height_of_a_row = 25
        top_left = pygame.Vector2(12, 25)
        arrow_col = top_left.x
        planet_col = arrow_col + 9
        label_col = planet_col + 33
        system = self.game.galaxy.systems[system_id]
        for orbit in range(MAX_ORBITS):
            row_middle = top_left.y + orbit * height_of_a_row + height_of_a_row / 2
            self.draw_orbit_arrow(arrow_col, row_middle)
            if planet_id := system.orbits[orbit]:
                self.draw_orbit_planet(planet_id, planet_col, row_middle)
                self.draw_orbit_text(planet_id, label_col, row_middle)

    #####################################################################################################
    def draw_orbit_arrow(self, arrow_col: float, row_middle: float) -> None:
        # Draw the arrow
        image_size = self.images[ImageNames.ORBIT_ARROW].get_size()
        arrow_dest = pygame.Rect(
            arrow_col,
            row_middle - image_size[1] / 2,
            image_size[0],
            image_size[1],
        )
        self.screen.blit(self.images[ImageNames.ORBIT_ARROW], arrow_dest)

    #####################################################################################################
    def draw_orbit_planet(self, planet_id: PlanetId, planet_col: float, row_middle: float) -> None:
        # Draw the planet image
        planet = self.game.galaxy.planets[planet_id]
        match planet.category:
            case PlanetCategory.ASTEROID:
                image = self.images["orbit_asteroid"]
            case PlanetCategory.GAS_GIANT:
                image = self.images["orbit_gas_giant"]
            case _:
                image = self.images[f"orbit_{planet.climate}_{planet.size}"]
        image_size = image.get_size()
        planet_dest = pygame.Rect(
            planet_col,
            row_middle - image_size[1] / 2,
            image_size[0],
            image_size[1],
        )
        self.screen.blit(image, planet_dest)
        if planet.category == PlanetCategory.PLANET:
            rect = pygame.Rect(planet_dest.left, planet_dest.top, planet_dest.width, planet_dest.height)
            pygame.draw.rect(self.screen, "purple", rect, width=1)
            self.planet_rects[planet] = rect

    #####################################################################################################
    def draw_orbit_text(self, planet_id: PlanetId, label_col: float, row_middle: float) -> None:
        # Draw the text
        planet = self.game.galaxy.planets[self.planet_id]
        text = self.orbit_label(planet_id)
        label_surface = self.label_font.render(text, True, "white")
        image_size = label_surface.get_size()
        label_dest = pygame.Rect(
            label_col,
            row_middle - image_size[1] / 2,
            label_surface.get_size()[0],
            label_surface.get_size()[1],
        )
        self.screen.blit(label_surface, label_dest)
        if planet.owner:
            self.detail_rect = label_dest
            pygame.draw.rect(self.screen, "purple", label_dest, width=1)

    #####################################################################################################
    def orbit_label(self, planet_id: PlanetId) -> str:
        """Empire name (pop/max)"""
        owner = ""
        planet = self.game.galaxy.planets[planet_id]
        match planet.category:
            case PlanetCategory.PLANET:
                owner = self.game.galaxy.empires[planet.owner].name if planet.owner else planet.name
            case PlanetCategory.ASTEROID:
                owner = "Asteroids"
            case PlanetCategory.GAS_GIANT:
                owner = "Gas Giant"
        pop = f"({planet.current_population()}/{planet.max_population()})" if planet.current_population() else ""
        return f"{owner} {pop}"

    #####################################################################################################
    def mouse_pos(self, event: pygame.event):
        """ """
        if self.worker:
            match self.worker[0]:
                case PopulationJobs.FARMERS:
                    image = self.images[ImageNames.FARMER]
                case PopulationJobs.WORKERS:
                    image = self.images[ImageNames.WORKER]
                case PopulationJobs.SCIENTISTS:
                    image = self.images[ImageNames.SCIENTIST]
                case _:
                    image = None
            delta = 0
            for _ in range(self.worker[1]):
                self.screen.blit(image, pygame.mouse.get_pos() + pygame.Vector2(delta, 0))
                delta += image.get_size()[0]

    #####################################################################################################
    def button_right_down(self):
        self.display_mode = DisplayMode.GALAXY

    #####################################################################################################
    def button_up(self):
        """Mouse button up - if we are moving workers then put them down"""
        if not self.worker:
            return
        planet = self.game.galaxy.planets[self.planet_id]
        farm_target_rect = pygame.Rect(307, 60, 205, 30)
        work_target_rect = pygame.Rect(307, 90, 205, 30)
        science_target_rect = pygame.Rect(307, 120, 205, 30)
        if farm_target_rect.collidepoint(pygame.mouse.get_pos()):
            planet.move_workers(self.worker[1], self.worker[0], PopulationJobs.FARMERS)
        if work_target_rect.collidepoint(pygame.mouse.get_pos()):
            planet.move_workers(self.worker[1], self.worker[0], PopulationJobs.WORKERS)
        if science_target_rect.collidepoint(pygame.mouse.get_pos()):
            planet.move_workers(self.worker[1], self.worker[0], PopulationJobs.SCIENTISTS)

        self.worker = None

    #####################################################################################################
    def loop(self, planet_id: PlanetId) -> DisplayMode:
        self.planet_id = planet_id
        self.display_mode = DisplayMode.PLANET
        while True:
            self.event_loop()

            match self.display_mode:
                case DisplayMode.PLANET_BUILD:
                    self.building_choice_window.loop(planet_id)
                    self.display_mode = DisplayMode.PLANET
                case DisplayMode.PLANET_DETAILS:
                    pass
                case DisplayMode.PLANET:
                    pass
                case _:
                    return self.display_mode

    #####################################################################################################
    def button_left_down(self) -> None:
        """Someone pressed the left button"""

        if self.buttons[PlanetButtons.BUILD].clicked():
            self.display_mode = DisplayMode.PLANET_BUILD
            return

        if self.buttons[PlanetButtons.RETURN].clicked():
            self.display_mode = DisplayMode.GALAXY
            return

        if self.display_mode == DisplayMode.PLANET_DETAILS and self.details_textbox.close_button.clicked():
            self.display_mode = DisplayMode.PLANET
            return

        # Change to look at a different planet in the same system
        for planet, rect in self.planet_rects.items():
            if rect.collidepoint(pygame.mouse.get_pos()):
                self.planet = planet
                self.display_mode = DisplayMode.PLANET
                return

        # Get planet details
        if self.detail_rect and self.detail_rect.collidepoint(pygame.mouse.get_pos()):
            self.display_mode = DisplayMode.PLANET_DETAILS
            return

        for job, rect in self.worker_rects.items():
            if rect.collidepoint(pygame.mouse.get_pos()):
                self.worker = job
                return


#####################################################################################################
def load_images() -> dict[ImageNames, pygame.Surface]:
    start = time.time()
    images = {}
    images[ImageNames.WINDOW] = load_image("COLPUPS.LBX", 5, palette_index=2)
    images[ImageNames.ORBIT_ARROW] = load_image("COLSYSDI.LBX", 64, palette_index=2)
    images[ImageNames.RETURN_BUTTON] = load_image("COLPUPS.LBX", 4, palette_index=2)
    images[ImageNames.BUILD_BUTTON] = load_image("COLPUPS.LBX", 1, palette_index=2)
    images |= load_climate_images()
    images |= load_orbit_images()
    images |= load_resource_images()
    images |= load_race_images()
    images |= load_construction_images()
    images |= load_government_images()

    end = time.time()
    print(f"Planet: Loaded {len(images)} in {end-start} seconds")
    return images


#####################################################################################################
def load_construction_images() -> dict[ImageNames, pygame.Surface]:
    images = {}
    return images


#####################################################################################################
def load_race_images() -> dict[ImageNames, pygame.Surface]:
    """Load farmer/worker/scientist/etc. race images"""
    # 1  Farmer
    # 2  Unknown
    # 3  Worker
    # 4  Scientist?
    # 5  Scientist?
    # 6  Marine
    # 7  Militia
    # 8  Mech?
    # 9  Tank
    # 10 Mech
    # 11 Spy?
    # 12 Prisoner
    images = {}
    images[ImageNames.FARMER] = load_image("RACEICON.LBX", 0, palette_index=2)
    images[ImageNames.WORKER] = load_image("RACEICON.LBX", 3, palette_index=2)
    images[ImageNames.SCIENTIST] = load_image("RACEICON.LBX", 5, palette_index=2)

    return images


#####################################################################################################
def load_government_images() -> dict[ImageNames, pygame.Surface]:
    images = {}
    images["government_Feudal"] = load_image("COLONY2.LBX", 19, palette_index=2)

    return images


#####################################################################################################
def load_resource_images() -> dict[ImageNames, pygame.Surface]:
    images = {}
    images[ImageNames.FOOD_1] = load_image("COLONY2.LBX", 0, palette_index=2)
    images[ImageNames.WORK_1] = load_image("COLONY2.LBX", 1, palette_index=2)
    images[ImageNames.SCIENCE_1] = load_image("COLONY2.LBX", 2, palette_index=2)
    images[ImageNames.MONEY_1] = load_image("COLONY2.LBX", 3, palette_index=2)
    images[ImageNames.FOOD_X] = load_image("COLONY2.LBX", 4, palette_index=2)
    images[ImageNames.WORK_X] = load_image("COLONY2.LBX", 5, palette_index=2)
    images[ImageNames.SCIENCE_X] = load_image("COLONY2.LBX", 6, palette_index=2)
    images[ImageNames.MONEY_X] = load_image("COLONY2.LBX", 7, palette_index=2)
    images[ImageNames.HUNGER_1] = load_image("COLONY2.LBX", 8, palette_index=2)
    images[ImageNames.POLLUTION_1] = load_image("COLONY2.LBX", 9, palette_index=2)
    images[ImageNames.IGNORANCE_1] = load_image("COLONY2.LBX", 10, palette_index=2)
    images[ImageNames.DEBT_1] = load_image("COLONY2.LBX", 11, palette_index=2)
    images[ImageNames.HUNGER_X] = load_image("COLONY2.LBX", 12, palette_index=2)
    images[ImageNames.POLLUTION_X] = load_image("COLONY2.LBX", 13, palette_index=2)
    images[ImageNames.IGNORANCE_X] = load_image("COLONY2.LBX", 14, palette_index=2)
    images[ImageNames.DEBT_X] = load_image("COLONY2.LBX", 15, palette_index=2)
    images[ImageNames.HAPPY] = load_image("COLONY2.LBX", 16, palette_index=2)

    return images


#####################################################################################################
def load_orbit_images() -> dict[str, pygame.Surface]:
    images = {}
    index = 6

    for climate in [
        PlanetClimate.TOXIC,
        PlanetClimate.RADIATED,
        PlanetClimate.BARREN,
        PlanetClimate.DESERT,
        PlanetClimate.TUNDRA,
        PlanetClimate.OCEAN,
        PlanetClimate.SWAMP,
        PlanetClimate.ARID,
        PlanetClimate.TERRAN,
        PlanetClimate.GAIA,
    ]:
        for size in [PlanetSize.TINY, PlanetSize.SMALL, PlanetSize.MEDIUM, PlanetSize.LARGE, PlanetSize.HUGE]:
            images[f"orbit_{climate}_{size}"] = load_image("COLSYSDI.LBX", index, palette_index=2)
            index += 1
    images["orbit_gas_giant"] = load_image("COLSYSDI.LBX", 62, palette_index=2)
    images["orbit_asteroid"] = load_image("COLSYSDI.LBX", 63, palette_index=2)
    return images


#####################################################################################################
def load_climate_images() -> dict[str, pygame.Surface]:
    images = {}
    index = 0
    for climate in [
        PlanetClimate.TOXIC,
        PlanetClimate.RADIATED,
        PlanetClimate.BARREN,
        PlanetClimate.DESERT,
        PlanetClimate.TUNDRA,
        PlanetClimate.OCEAN,
        PlanetClimate.SWAMP,
        PlanetClimate.ARID,
        PlanetClimate.TERRAN,
        PlanetClimate.GAIA,
    ]:
        for number in range(3):
            images[f"surface_{climate}_{number}"] = load_image("PLANETS.LBX", index, palette_index=2)
            index += 1
    return images


# EOF
