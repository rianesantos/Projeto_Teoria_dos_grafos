"""
Pratica 1 - Grafos: Parte 2 - Alocacao de Canais Wi-Fi
================================================================

Le um grafo nao-direcionado e sem pesos representando a interferencia
entre pontos de acesso (APs) de uma rede Wi-Fi, e calcula uma
coloracao valida que usa o menor numero possivel de cores (canais),
isto e, o numero cromatico exato χ(G).

Escolha do algoritmo:
    Um algoritmo guloso simples (ordem arbitraria, ou mesmo DSatur)
    NAO garante encontrar o numero cromatico otimo -- ele apenas
    fornece um limite superior. Como o enunciado pede o menor numero
    possivel de canais, usamos busca com backtracking (branch and
    bound), tentando primeiro k = 1, depois k = 2, 3, ... ate
    encontrar o menor k para o qual existe coloracao valida.

    Para tornar o backtracking eficiente, os vertices sao ordenados
    por grau decrescente (heuristica que tende a podar a busca mais
    cedo, similar a motivacao do DSatur), e a cada vertice tentamos
    apenas cores ainda nao usadas pelos vizinhos ja coloridos.

    Esse algoritmo encontra o numero cromatico exato, mas tem
    complexidade exponencial no pior caso -- adequado aqui pois os
    grafos de entrada sao pequenos/medios.

Uso:
    python3 coloracao.py <arquivo_entrada> <arquivo_saida>

Exemplo:
    python3 coloracao.py ../dados/grafo_wifi_p.txt saida_parte2_p.txt
"""

import sys


def ler_grafo(caminho):
    """Le o grafo no formato:
    <num_vertices>\\t<num_arestas>
    <u>\\t<v>   (repetido num_arestas vezes, sem peso)
    """
    with open(caminho, "r", encoding="utf-8") as f:
        linhas = [linha.rstrip("\n") for linha in f if linha.strip() != ""]

    n, m = map(int, linhas[0].split("\t"))

    arestas = []
    for i in range(1, 1 + m):
        u, v = linhas[i].split("\t")
        arestas.append((int(u), int(v)))

    return n, m, arestas


def montar_adjacencia(n, arestas):
    adj = [set() for _ in range(n)]
    for u, v in arestas:
        adj[u].add(v)
        adj[v].add(u)
    return adj


def colorir_com_k_cores(n, adj, k, ordem):
    """Tenta colorir o grafo com exatamente k cores disponiveis usando
    backtracking. Retorna a lista de cores (1-indexada) por vertice
    em caso de sucesso, ou None caso k cores nao sejam suficientes."""
    cor = [0] * n

    def backtrack(pos):
        if pos == n:
            return True

        v = ordem[pos]
        cores_vizinhas = {cor[u] for u in adj[v] if cor[u] != 0}

        for c in range(1, k + 1):
            if c not in cores_vizinhas:
                cor[v] = c
                if backtrack(pos + 1):
                    return True
                cor[v] = 0

        return False

    if backtrack(0):
        return cor
    return None


def numero_cromatico_exato(n, adj):
    """Encontra o numero cromatico exato testando k = 1, 2, 3, ...
    Os vertices sao ordenados por grau decrescente para acelerar a
    busca (poda mais cedo nos vertices mais restritos)."""
    ordem = sorted(range(n), key=lambda v: -len(adj[v]))

    k = 1
    while True:
        resultado = colorir_com_k_cores(n, adj, k, ordem)
        if resultado is not None:
            return k, resultado
        k += 1


def validar_coloracao(arestas, cor):
    return all(cor[u] != cor[v] for u, v in arestas)


def resolver(caminho_entrada, caminho_saida):
    n, m, arestas = ler_grafo(caminho_entrada)
    adj = montar_adjacencia(n, arestas)

    k, cor = numero_cromatico_exato(n, adj)

    assert validar_coloracao(arestas, cor), "Coloracao invalida gerada (bug)!"
    assert len(set(cor)) == k, "NUM_CORES nao bate com cores efetivamente usadas (bug)!"

    algoritmo = "Backtracking (busca exata por k crescente)"
    justificativa = (
        "Algoritmos gulosos (incluindo DSatur) nao garantem encontrar o "
        "numero cromatico otimo, apenas um limite superior. Por isso, "
        "buscamos o menor k para o qual existe coloracao valida via "
        "backtracking, com poda por ordenacao decrescente de grau."
    )

    coloracao_str = " ".join(f"{v}={cor[v]}" for v in range(n))

    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.write(f"ALGORITMO: {algoritmo}\n")
        f.write(f"JUSTIFICATIVA: {justificativa}\n")
        f.write(f"NUM_CORES: {k}\n")
        f.write(f"COLORACAO: {coloracao_str}\n")

    print(f"[{caminho_entrada}] chi(G) = {k}")
    print(f"  coloracao: {coloracao_str}")
    print(f"  -> saida gravada em {caminho_saida}")


def main():
    if len(sys.argv) != 3:
        print("Uso: python3 coloracao.py <arquivo_entrada> <arquivo_saida>")
        sys.exit(1)

    resolver(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
