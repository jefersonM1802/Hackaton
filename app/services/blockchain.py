import hashlib

class BlockchainService:
    @staticmethod
    def generate_hash(filepath):
        """
        Lee un archivo en bloques binarios y genera un SHA-256.
        Esto garantiza la INTEGRIDAD del documento.
        """
        sha256_hash = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                # Leemos en bloques de 4KB para no saturar la memoria RAM
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except FileNotFoundError:
            return None

    @staticmethod
    def verify_integrity(filepath, original_hash):
        """
        Compara el hash actual con el guardado en la BD.
        Retorna True si el documento es original.
        """
        current_hash = BlockchainService.generate_hash(filepath)
        return current_hash == original_hash