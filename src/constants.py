# src/constants.py

import os

# --- Application Info ---
CREDITS_APP_NAME = "Application: Quebra Fone"
CREDITS_DEVELOPER = "Developed by: Diego Soprana Gomes"

# --- Default Directory Names ---
DEFAULT_EFEITOS_DIR = "efeitos"
DEFAULT_EMOJIS_DIR = "emojis"
DEFAULT_ASSETS_DIR = "assets"

# --- UI Colors (RGB tuples) ---
BG_COLOR_SELECTION = (230, 230, 230)
BG_COLOR_MAIN = (255, 255, 255)
BG_COLOR_LOADING = (40, 44, 52)

TEXT_COLOR_DARK = (0, 0, 0)
TEXT_COLOR_LIGHT = (255, 255, 255)
TEXT_COLOR_CREDITS = (180, 180, 180)

SELECTION_BTN_COLOR = (50, 150, 255)
SELECTION_BTN_TEXT_COLOR = TEXT_COLOR_LIGHT

EFFECT_BTN_TEXT_COLOR = TEXT_COLOR_LIGHT
EFFECT_BTN_PLAYING_COLOR = (150, 200, 255)

SHADOW_COLOR = (180, 180, 180)

# Pagination Button Style
PAGINATION_BTN_COLOR = (70, 170, 255)
PAGINATION_BTN_TEXT_COLOR = TEXT_COLOR_LIGHT
PAGINATION_BTN_DISABLED_COLOR = (200, 200, 200)

# Sorting Button Style (can reuse pagination style or define new)
SORTING_BTN_COLOR = PAGINATION_BTN_COLOR # Reusing pagination button color
SORTING_BTN_TEXT_COLOR = PAGINATION_BTN_TEXT_COLOR # Reusing pagination text color
SORTING_BTN_DISABLED_COLOR = PAGINATION_BTN_DISABLED_COLOR # Reusing disabled color


# --- UI Dimensions and Spacing ---
SELECTION_BTN_WIDTH = 400
SELECTION_BTN_HEIGHT = 50
SELECTION_BTN_SPACING = 15

EFFECT_BTN_MIN_WIDTH = 200
EFFECT_BTN_HEIGHT = 70
EFFECT_BTN_SPACING_X = 20
EFFECT_BTN_SPACING_Y = 20
EFFECT_BTN_IDEAL_COLUMNS = 3

EMOJI_SIZE_EFFECT_BUTTON = int(EFFECT_BTN_HEIGHT * 0.75)
EFFECT_BTN_EMOJI_MARGIN_LEFT = 15
EMOJI_TEXT_SPACING = 10
EFFECT_BTN_TEXT_MARGIN_RIGHT = 10

BUTTON_BORDER_RADIUS = 8
SHADOW_OFFSET = 3

UI_MARGIN = 10
HEADER_MARGIN = 40

FECHAR_BTN_WIDTH = 30
FECHAR_BTN_HEIGHT = 25
FECHAR_BTN_MARGIN = UI_MARGIN
FECHAR_BTN_COLOR = (255, 0, 0)
FECHAR_BTN_TEXT_COLOR = TEXT_COLOR_LIGHT

# --- Pagination Settings ---
PAGINATION_BTN_WIDTH = 100
PAGINATION_BTN_HEIGHT = 30
PAGINATION_BTN_SPACING = 10
PAGINATION_AREA_HEIGHT = PAGINATION_BTN_HEIGHT + PAGINATION_BTN_SPACING * 2

# --- Sorting Settings ---
# Define os tipos de ordenação suportados (valor interno, texto para UI)
SORT_ALFANUMERIC_ASC = "alfanumeric_asc"
SORT_ALFANUMERIC_DESC = "alfanumeric_desc"
# REMOVA ou COMENTE a linha abaixo:
# SORT_LAST_MODIFIED = "last_modified" # Ordena do mais recente para o mais antigo
# ADICIONE a constante para ordenação por data de criação:
SORT_CREATION_TIME = "creation_time" # Ordena do mais recente para o mais antigo pela data de criação


DEFAULT_SORT_ORDER = SORT_ALFANUMERIC_ASC # Ordem padrão se não especificada no config
# Opcional: Altere a ordem padrão para data de criação se preferir:
# DEFAULT_SORT_ORDER = SORT_CREATION_TIME


# Lista de opções de ordenação para a UI (valor_interno, texto_display)
SORT_OPTIONS = [
    (SORT_ALFANUMERIC_ASC, "Name A-Z"),
    (SORT_ALFANUMERIC_DESC, "Name Z-A"),
    # REMOVA ou COMENTE a tupla de Last Modified:
    # (SORT_LAST_MODIFIED, "Recente"),
    # ADICIONE a tupla para Creation Time:
    (SORT_CREATION_TIME, "Last Add") # Texto para exibir na UI
]

# Dimensões e espaçamento para os botões de ordenação
SORTING_BTN_WIDTH = 100 # Largura de cada botão de ordenação
SORTING_BTN_HEIGHT = 30 # Altura de cada botão de ordenação
SORTING_BTN_SPACING = 10 # Espaçamento entre botões de ordenação
# Altura total da área reservada para os botões de ordenação
SORTING_AREA_HEIGHT = SORTING_BTN_HEIGHT + UI_MARGIN * 2


# --- Asset Paths ---
LOADING_GIF_RELATIVE_PATH = os.path.join(DEFAULT_ASSETS_DIR, "loading.gif")
ICON_RELATIVE_PATH = os.path.join(DEFAULT_ASSETS_DIR, "icon.png")


# --- Other Constants ---
LOADING_TEXT_COLOR = TEXT_COLOR_LIGHT
CREDITS_TEXT_COLOR = TEXT_COLOR_CREDITS