""" Display Planet Details"""

import time
from enum import Enum, StrEnum, auto
from typing import Optional

import pygame
from MooToo.base_graphics import BaseGraphics
from MooToo.textbox_window import TextBoxWindow
from MooToo.constants import PlanetClimate, PlanetCategory, PlanetSize, PopulationJobs
from MooToo.system import System, MAX_ORBITS
from MooToo.planet import Planet
from MooToo.gui_button import Button
from MooToo.building_choice_window import BuildingChoiceWindow


#####################################################################################################
class PlanetButtons(StrEnum):
    RETURN = auto()
    BUILD = auto()


#####################################################################################################
class PlanetDisplayMode(Enum):
    NORMAL = auto()
    BUILD = auto()
    DETAILS = auto()


#####################################################################################################
#####################################################################################################
class PlanetWindow(BaseGraphics):
    def __init__(self, screen: pygame.Surface, game: "Game"):
        """ """
        super().__init__(game)
        self.screen = screen
        self.planet = None
        self.images = self.load_images()
        self.planet_rects: dict[tuple[float, float, float, float], Planet] = {}
        self.detail_rect: Optional[pygame.Rect] = None
        self.colony_font = pygame.font.SysFont("Ariel", 18, bold=True)
        self.display_mode = PlanetDisplayMode.NORMAL
        self.building_choice_window = BuildingChoiceWindow(screen, game)
        self.buttons = {
            PlanetButtons.RETURN: Button(self.images["return_button"], pygame.Vector2(555, 460)),
            PlanetButtons.BUILD: Button(self.images["build_button"], pygame.Vector2(525, 123)),
        }
        self.details_textbox = TextBoxWindow(screen, game)

    #####################################################################################################
    def load_images(self) -> dict[str, pygame.Surface]:
        start = time.time()
        images = {}
        images["window"] = self.load_image("COLPUPS.LBX", 5, palette_index=2)
        images["orbit_arrow"] = self.load_image("COLSYSDI.LBX", 64, palette_index=2)
        images["return_button"] = self.load_image("COLPUPS.LBX", 4, palette_index=2)
        images["build_button"] = self.load_image("COLPUPS.LBX", 1, palette_index=2)
        images |= self.load_climate_images()
        images |= self.load_orbit_images()
        images |= self.load_resource_images()
        images |= self.load_race_images()
        images |= self.load_construction_images()
        images |= self.load_government_images()

        end = time.time()
        print(f"Planet: Loaded {len(images)} in {end-start} seconds")
        return images

    #####################################################################################################
    def load_construction_images(self) -> dict[str, pygame.Surface]:
        images = {}
        return images

    #####################################################################################################
    def load_race_images(self) -> dict[str, pygame.Surface]:
        """Load farmer/worker/scientist/etc race images"""
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
        images["farmer"] = self.load_image("RACEICON.LBX", 0, palette_index=2)
        images["worker"] = self.load_image("RACEICON.LBX", 3, palette_index=2)
        images["scientist"] = self.load_image("RACEICON.LBX", 5, palette_index=2)

        return images

    #####################################################################################################
    def load_government_images(self) -> dict[str, pygame.Surface]:
        images = {}
        images["government_Feudal"] = self.load_image("COLONY2.LBX", 19, palette_index=2)

        return images

    #####################################################################################################
    def load_resource_images(self) -> dict[str, pygame.Surface]:
        images = {}
        images["food_1"] = self.load_image("COLONY2.LBX", 0, palette_index=2)
        images["work_1"] = self.load_image("COLONY2.LBX", 1, palette_index=2)
        images["science_1"] = self.load_image("COLONY2.LBX", 2, palette_index=2)
        images["coin_1"] = self.load_image("COLONY2.LBX", 3, palette_index=2)
        images["food_5"] = self.load_image("COLONY2.LBX", 4, palette_index=2)
        images["work_5"] = self.load_image("COLONY2.LBX", 5, palette_index=2)
        images["science_5"] = self.load_image("COLONY2.LBX", 6, palette_index=2)
        images["coin_5"] = self.load_image("COLONY2.LBX", 7, palette_index=2)
        images["happy"] = self.load_image("COLONY2.LBX", 16, palette_index=2)

        return images

    #####################################################################################################
    def load_orbit_images(self) -> dict[str, pygame.Surface]:
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
                images[f"orbit_{climate}_{size}"] = self.load_image("COLSYSDI.LBX", index, palette_index=2)
                index += 1
        images["orbit_gas_giant"] = self.load_image("COLSYSDI.LBX", 62, palette_index=2)
        images["orbit_asteroid"] = self.load_image("COLSYSDI.LBX", 63, palette_index=2)
        return images

    #####################################################################################################
    def load_climate_images(self) -> dict[str, pygame.Surface]:
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
                images[f"surface_{climate}_{number}"] = self.load_image("PLANETS.LBX", index, palette_index=2)
                index += 1
        return images

    #####################################################################################################
    def details_text(self) -> list[str]:
        pop_str = f"{self.planet.current_population()}/{self.planet.max_population()}"
        return [
            f"{self.planet.name} - {self.planet.owner.name} Colony",
            f"{self.planet.size} {self.planet.climate}",
            f"Mineral {self.planet.richness}",
            f"{self.planet.gravity} G",
            "",
            f"{'Base food per':<20}{self.planet.food_per():>30}",
            f"{'Base industry per':<20}{self.planet.production_per():>30}",
            f"{'Base research per':<20}{self.planet.research_per():>30}",
            "",
            f"{'Morale':<20}{self.planet.morale()*10:>29}%",
            "",
            f"{'Population':<20}{pop_str:>30}",
        ]

    #####################################################################################################
    def draw(self, system: System):
        self.draw_centered_image(self.images[self.planet.climate_image])
        if self.display_mode == PlanetDisplayMode.BUILD:
            self.building_choice_window.draw(self.planet)
            return
        if self.display_mode == PlanetDisplayMode.DETAILS:
            self.details_textbox.draw(self.details_text(), self.title_font)
            return

        self.window = self.draw_centered_image(self.images["window"])
        self.draw_orbits(system)
        self.draw_resources(self.planet)
        self.draw_pop_label(self.planet)
        self.draw_population(self.planet)
        self.draw_currently_building(self.planet)
        self.draw_government(self.planet)
        self.draw_morale(self.planet)
        self.draw_buildings(self.planet)
        for button in self.buttons.values():
            button.draw(self.screen)
        label_surface = self.colony_font.render(f"{self.planet.name}", True, "white")
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
    def draw_buildings(self, planet: Planet) -> None:
        """Draw the current buildings on the planet"""
        top_left = pygame.Vector2(8, 170)
        for building in planet.buildings:
            text = self.text_font.render(planet.galaxy.get_building(building).name, True, "purple")
            self.screen.blit(text, top_left)
            top_left.y += text.get_size()[1]

    #####################################################################################################
    def draw_morale(self, planet: Planet) -> None:
        top_left = pygame.Vector2(340, 31)
        if not planet.owner:
            return
        for _ in range(planet.morale()):
            pos = self.screen.blit(self.images["happy"], top_left)
            top_left.x += pos.width

    #####################################################################################################
    def draw_government(self, planet: Planet) -> None:
        top_left = pygame.Vector2(309, 31)
        if not planet.owner:
            return
        government = planet.owner.government
        image = self.images[f"government_{government}"]
        self.screen.blit(image, top_left)

    #####################################################################################################
    def draw_currently_building(self, planet: Planet) -> None:
        if not planet.build_queue:
            return
        top_left = pygame.Vector2(527, 27)
        building = self.planet.build_queue[0]
        text = self.text_font.render(building.name, True, "purple")
        self.screen.blit(text, top_left)

    #####################################################################################################
    def draw_population(self, planet: Planet) -> None:
        """Draw farmers etc"""
        dest = pygame.Vector2(309, 62)
        self.draw_population_sequence(dest, self.images["farmer"], planet.jobs[PopulationJobs.FARMER])

        dest = pygame.Vector2(309, 92)
        self.draw_population_sequence(dest, self.images["worker"], planet.jobs[PopulationJobs.WORKERS])

        dest = pygame.Vector2(309, 122)
        self.draw_population_sequence(dest, self.images["scientist"], planet.jobs[PopulationJobs.SCIENTISTS])

    #####################################################################################################
    def draw_population_sequence(
        self, top_left: pygame.Vector2, worker_image: pygame.Surface, value: int
    ) -> pygame.Vector2:
        """Display a sequence of population images"""
        for _ in range(value):
            self.screen.blit(worker_image, top_left)
            top_left.x += worker_image.get_size()[0]
        return top_left

    #####################################################################################################
    def draw_resources(self, planet: Planet) -> None:
        """Draw the income, food, etc."""
        self.draw_income(planet)
        self.draw_food(planet)
        self.draw_work(planet)
        self.draw_science(planet)

    #####################################################################################################
    def draw_income(self, planet: Planet) -> None:
        income = planet.money_production()
        cost = planet.money_cost()
        dest = pygame.Vector2(126, 31)
        self.draw_resource(dest, self.images["coin_1"], self.images["coin_5"], income, cost)

    #####################################################################################################
    def draw_food(self, planet: Planet) -> None:
        income = planet.food_production()
        cost = planet.food_lack()
        dest = pygame.Vector2(126, 60)
        self.draw_resource(dest, self.images["food_1"], self.images["food_5"], income, cost)

    #####################################################################################################
    def draw_work(self, planet: Planet) -> None:
        income = planet.work_production()
        cost = planet.pollution()
        dest = pygame.Vector2(126, 90)
        self.draw_resource(dest, self.images["work_1"], self.images["work_5"], income, cost)

    #####################################################################################################
    def draw_science(self, planet: Planet) -> None:
        labs = planet.science_production()
        dest = pygame.Vector2(126, 120)
        self.draw_resource(dest, self.images["science_1"], self.images["science_5"], labs, 0)

    #####################################################################################################
    def draw_resource(
        self, top_left: pygame.Vector2, image_1: pygame.Surface, image_5: pygame.Surface, in_value: int, out_value: int
    ) -> None:
        """Display a resource"""
        if out_value:
            top_left = self.draw_resource_sequence(top_left, image_1, image_5, out_value)
            top_left.x += 10  # Gap
        surplus = in_value - out_value
        self.draw_resource_sequence(top_left, image_1, image_5, surplus)

    #####################################################################################################
    def draw_resource_sequence(
        self, top_left: pygame.Vector2, image_1: pygame.Surface, image_5: pygame.Surface, value: int
    ) -> pygame.Vector2:
        """Display a sequence of resource images"""
        for _ in range(value // 5):
            self.screen.blit(image_5, top_left)
            top_left.x += image_5.get_size()[0]
        for _ in range(value % 5):
            self.screen.blit(image_1, top_left)
            top_left.x += image_1.get_size()[0]
        return top_left

    #####################################################################################################
    def draw_pop_label(self, planet: Planet) -> None:
        text = f"Pop {int(planet._population / 1000):,}k (+{int(planet.population_increment() / 1000):,}k)"
        text_surface = self.label_font.render(text, True, "white")
        text_size = text_surface.get_size()
        self.screen.blit(text_surface, pygame.Rect(640 - text_size[0], 0, text_size[0], text_size[1]))

    #####################################################################################################
    def draw_orbits(self, system: System):
        """Draw the system summary"""
        height_of_a_row = 25
        top_left = pygame.Vector2(12, 25)
        arrow_col = top_left.x
        planet_col = arrow_col + 9
        label_col = planet_col + 33
        for orbit in range(MAX_ORBITS):
            row_middle = top_left.y + orbit * height_of_a_row + height_of_a_row / 2
            self.draw_orbit_arrow(arrow_col, row_middle)
            if planet := system.orbits[orbit]:
                self.draw_orbit_planet(planet, planet_col, row_middle)
                self.draw_orbit_text(planet, label_col, row_middle)

    #####################################################################################################
    def draw_orbit_arrow(self, arrow_col: float, row_middle: float) -> None:
        # Draw the arrow
        image_size = self.images["orbit_arrow"].get_size()
        arrow_dest = pygame.Rect(
            arrow_col,
            row_middle - image_size[1] / 2,
            image_size[0],
            image_size[1],
        )
        self.screen.blit(self.images["orbit_arrow"], arrow_dest)

    #####################################################################################################
    def draw_orbit_planet(self, planet: Planet, planet_col: float, row_middle: float) -> None:
        # Draw the planet image
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
            self.planet_rects[(planet_dest.left, planet_dest.top, planet_dest.width, planet_dest.height)] = planet

    #####################################################################################################
    def draw_orbit_text(self, planet: Planet, label_col: float, row_middle: float) -> None:
        # Draw the text
        text = self.orbit_label(planet)
        label_surface = self.label_font.render(text, True, "white")
        image_size = label_surface.get_size()
        label_dest = pygame.Rect(
            label_col,
            row_middle - image_size[1] / 2,
            label_surface.get_size()[0],
            label_surface.get_size()[1],
        )
        self.screen.blit(label_surface, label_dest)
        if planet == self.planet:
            self.detail_rect = label_dest

    #####################################################################################################
    def orbit_label(self, planet: Planet) -> str:
        """Empire name (pop/max)"""
        owner = ""
        match planet.category:
            case PlanetCategory.PLANET:
                owner = planet.owner.name if planet.owner else planet.name
            case PlanetCategory.ASTEROID:
                owner = "Asteroids"
            case PlanetCategory.GAS_GIANT:
                owner = "Gas Giant"
        pop = f"({planet.current_population()}/{planet.max_population()})" if planet.current_population() else ""
        return f"{owner} {pop}"

    #####################################################################################################
    def button_left_down(self) -> bool:
        if self.display_mode == PlanetDisplayMode.BUILD:
            if self.building_choice_window.button_left_down():
                self.display_mode = PlanetDisplayMode.NORMAL
                return False
        if self.display_mode == PlanetDisplayMode.DETAILS:
            if self.details_textbox.button_left_down():
                self.display_mode = PlanetDisplayMode.NORMAL
                return False
        if self.buttons[PlanetButtons.RETURN].clicked():
            self.planet = None
            return True
        if self.buttons[PlanetButtons.BUILD].clicked():
            self.display_mode = PlanetDisplayMode.BUILD

        for sys_rect, planet in self.planet_rects.items():
            r = pygame.Rect(sys_rect[0], sys_rect[1], sys_rect[2], sys_rect[3])
            if r.collidepoint(pygame.mouse.get_pos()):
                self.planet = planet
        if self.detail_rect.collidepoint(pygame.mouse.get_pos()):
            self.display_mode = PlanetDisplayMode.DETAILS
        return False


# EOF
