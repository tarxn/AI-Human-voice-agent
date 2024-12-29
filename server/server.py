import torch
from moshi_mlx.local import run_server

if __name__ == "__main__":
    # Determine the appropriate 
    device = "mps" if torch.backends.mps.is_available() else "cpu"

    print(f"Using device: {device}")

    run_server(
        gradio_tunnel=False,
        hf_repo="kyutai/moshika-mlx-q4",  # Use a compatible pretrained model for moshi_mlx
        device=device,
        quantization=4  # Use 4-bit quantization for better performance on macOS
    )
