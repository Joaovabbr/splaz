import os
import io

class LidarQuadrante:
    """
    Representa um quadrante LiDAR (MDS 2020) de São Paulo.
    Encapsula o conteúdo binário e metadados do arquivo .laz.
    """
    def __init__(self, codigo: str, conteudo_binario: bytes | None = None, nome_arquivo: str | None = None): 
        self.codigo = codigo
        self.conteudo_binario = conteudo_binario
        self.nome_arquivo = nome_arquivo

    @property
    def esta_carregado(self) -> bool:
        """Verifica se o conteúdo binário já está na memória."""
        return self.conteudo_binario is not None

    def save(self, pasta_destino: str) -> str:
        """
        Salva o conteúdo binário em disco.
        Retorna o caminho completo do arquivo salvo.
        """
        if not self.esta_carregado:
            raise ValueError(f"O quadrante {self.codigo} não possui dados em memória.")

        os.makedirs(pasta_destino, exist_ok=True)
        caminho_final = os.path.join(pasta_destino, self.nome_arquivo)

        with open(caminho_final, 'wb') as f:
            f.write(self.conteudo_binario)
        
        return caminho_final

    def to_laspy(self):
        """
        Retorna um objeto laspy.read() diretamente do conteúdo em memória.
        Requer a biblioteca 'laspy' instalada.
        """
        try:
            import laspy
            if self.esta_carregado:
                return laspy.read(io.BytesIO(self.conteudo_binario))
        except ImportError:
            raise ImportError("A biblioteca 'laspy' é necessária para converter dados em memória.")
        return None

    def __repr__(self):
        status = "Carregado" if self.esta_carregado else "Vazio"
        return f"<LidarQuadrante {self.codigo} | {status}>"