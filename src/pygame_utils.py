# src/pygame_utils.py

import pygame
from .constants import (
    FECHAR_BTN_WIDTH, FECHAR_BTN_HEIGHT, FECHAR_BTN_MARGIN, FECHAR_BTN_COLOR, FECHAR_BTN_TEXT_COLOR,
    BUTTON_BORDER_RADIUS, SHADOW_COLOR, SHADOW_OFFSET,
    PAGINATION_BTN_COLOR, PAGINATION_BTN_TEXT_COLOR, PAGINATION_BTN_DISABLED_COLOR,
    PAGINATION_BTN_WIDTH, PAGINATION_BTN_HEIGHT, PAGINATION_BTN_SPACING,
    TEXT_COLOR_DARK # Necessário para desenhar texto
)
import os

def load_icon(path, icon_size=(32, 32)):
    """
    Carrega uma imagem para ser usada como ícone da janela e a redimensiona.
    Retorna a surface redimensionada ou None em caso de erro.
    """
    # print(f"DEBUG load_icon: Received path: {path}") # Pode comentar prints de debug se não precisar mais
    if not os.path.exists(path):
        # print(f"⚠️ load_icon: Icon file not found at {path}") # Pode comentar prints de debug
        return None
    try:
        surface = pygame.image.load(path).convert_alpha()
        # print(f"DEBUG load_icon: Successfully loaded initial image surface.") # Pode comentar prints de debug
        # print(f"DEBUG load_icon: Initial size: {surface.get_size()}") # Pode comentar prints de debug

        # Redimensiona a imagem para o tamanho de ícone desejado
        scaled_surface = pygame.transform.scale(surface, icon_size)

        # print(f"DEBUG load_icon: Scaled image to size: {scaled_surface.get_size()}") # Pode comentar prints de debug
        return scaled_surface

    except pygame.error as e:
        print(f"⚠️ load_icon: Error loading or scaling image from {path}: {e}")
        return None
    except Exception as e:
        print(f"⚠️ load_icon: An unexpected error occurred loading or scaling image from {path}: {e}")
        return None

def draw_button(screen, rect, text, font, color, text_color, border_radius=BUTTON_BORDER_RADIUS, shadow_color=None, shadow_offset=SHADOW_OFFSET):
    """Desenha um botão genérico com sombra opcional e bordas arredondadas."""
    if shadow_color:
         shadow_rect = pygame.Rect(rect.x + shadow_offset, rect.y + shadow_offset, rect.width, rect.height)
         pygame.draw.rect(screen, shadow_color, shadow_rect, border_radius=border_radius)

    pygame.draw.rect(screen, color, rect, border_radius=border_radius)

    # Renderiza o texto e centraliza
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def draw_close_button(screen, font):
    """Desenha o botão de fechar customizado no canto superior direito."""
    screen_width, screen_height = screen.get_size()
    rect = pygame.Rect(
        screen_width - FECHAR_BTN_WIDTH - FECHAR_BTN_MARGIN,
        FECHAR_BTN_MARGIN,
        FECHAR_BTN_WIDTH,
        FECHAR_BTN_HEIGHT
    )
    draw_button(
        screen,
        rect,
        "X", # Texto do botão de fechar
        font, # Use a fonte principal
        FECHAR_BTN_COLOR,
        FECHAR_BTN_TEXT_COLOR,
        border_radius=BUTTON_BORDER_RADIUS, # Pode usar ou não, FECHAR_BTN_HEIGHT é pequeno
        shadow_color=None # Geralmente botões pequenos não tem sombra
    )
    return rect # Retorna o rect para detecção de clique

# Função para desenhar um botão de paginação (anterior/próximo)
def draw_pagination_button(screen, rect, text, font, enabled=True):
    """Desenha um botão de paginação, habilitado ou desabilitado."""
    color = PAGINATION_BTN_COLOR if enabled else PAGINATION_BTN_DISABLED_COLOR
    text_color = PAGINATION_BTN_TEXT_COLOR if enabled else TEXT_COLOR_DARK # Texto escuro para desabilitado
    draw_button(
        screen,
        rect,
        text,
        font,
        color,
        text_color,
        border_radius=BUTTON_BORDER_RADIUS,
        shadow_color=SHADOW_COLOR # Pode ter sombra
    )
    return rect # Retorna o rect para detecção de clique