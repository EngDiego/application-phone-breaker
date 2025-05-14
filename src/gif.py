# src/gif.py
# -*- coding: utf-8 -*-

import os
from PIL import Image, UnidentifiedImageError  # Importar Pillow
import pygame  # Importar Pygame para converter para Surface


def load_gif_frames(gif_path, size=None):
    """
    Carrega frames de um GIF (animado ou estático) e retorna como superfícies Pygame.
    Lida com GIFs de um único frame e GIFs animados.

    Args:
        gif_path (str): O caminho para o arquivo GIF.
        size (tuple, optional): Uma tupla (largura, altura) para redimensionar cada frame. Padrão: None.

    Returns:
        list: Uma lista de tuplas (pygame.Surface, int) onde o int é a duração do frame em ms.
              Retorna uma lista vazia em caso de erro ou arquivo não encontrado.
    """
    frames = []
    try:
        img = Image.open(gif_path)

        # Verifica se a imagem é animada. is_animated é um atributo que pode não existir
        # em todos os objetos Image, então usamos getattr.
        is_animated = getattr(img, "is_animated", False)

        # Obtém o número de frames. Para imagens não animadas ou onde n_frames não existe, usa 1.
        num_frames = getattr(img, "n_frames", 1)

        if not is_animated and num_frames == 1:
            print(
                f"⚠️ Arquivo '{os.path.basename(gif_path)}' contém apenas um frame. Tratando como imagem estática."
            )
        elif is_animated:
            print(
                f"✅ Carregando GIF animado '{os.path.basename(gif_path)}' com {num_frames} frames."
            )
        else:
            # Caso raro: imagem não marcada como animada mas com > 1 frame, ou vice-versa
            print(
                f"ℹ️ Arquivo '{os.path.basename(gif_path)}' ({img.format}) tem {num_frames} frames, animated={is_animated}."
            )

        for frame_index in range(num_frames):
            try:
                img.seek(
                    frame_index
                )  # Tenta ir para o frame (só faz algo em GIFs animados)
            except EOFError:
                # Pode acontecer se houver um problema na leitura dos frames
                print(f"⚠️ EOFError ao buscar frame {frame_index}. Parando leitura.")
                break
            except Exception as seek_e:
                print(
                    f"⚠️ Erro inesperado ao buscar frame {frame_index}: {seek_e}. Parando leitura."
                )
                break

            # Converte o frame para RGBA (necessário para transparência e compatibilidade Pygame)
            frame = img.convert("RGBA")

            # Redimensiona o frame se um tamanho for especificado
            if size:
                try:
                    # Use Image.Resampling.LANCZOS para melhor qualidade ao redimensionar
                    frame = frame.resize(size, Image.Resampling.LANCZOS)
                except Exception as resize_e:
                    print(f"⚠️ Erro ao redimensionar frame {frame_index}: {resize_e}")
                    # Continue without resizing this frame if possible, or break
                    if not frames:  # If first frame failed resize, maybe exit
                        return []

            # Converte o frame processado (RGBA, redimensionado) para uma superfície Pygame
            pygame_frame = pygame.image.frombytes(
                frame.tobytes(), frame.size, frame.mode
            ).convert_alpha()

            # Obtém a duração deste frame específico (somente relevante para GIFs animados)
            # Usa um valor padrão (100ms) se não especificado no GIF ou se for estático
            duration = img.info.get("duration", 100) if is_animated else 100

            frames.append((pygame_frame, duration))

        if not frames:  # Se a lista de frames estiver vazia por algum motivo
            print(
                f"❌ Não foi possível extrair frames do arquivo: {gif_path}. A lista de frames está vazia."
            )

        return frames

    except FileNotFoundError:
        print(f"❌ GIF/Imagem de carregamento não encontrado: {gif_path}")
        return []
    except UnidentifiedImageError:
        print(
            f"❌ Arquivo não é um formato de imagem reconhecido por Pillow ou está corrompido: {gif_path}"
        )
        return []
    except Exception as e:
        # Captura outros erros potenciais durante o processamento (abertura, seek, convert, etc.)
        print(f"❌ Erro inesperado ao carregar ou processar imagem '{gif_path}': {e}")
        # Opcional: descomente para ver o traceback completo
        # import traceback
        # traceback.print_exc()
        return []
