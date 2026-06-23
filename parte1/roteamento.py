"""
Pratica 1 - Grafos: Parte 1 - Roteamento em Rede de Backbone
================================================================

Le um grafo direcionado e ponderado representando uma rede de backbone
e calcula o caminho de menor custo entre um roteador de origem (S) e
um roteador de destino (T).

Escolha do algoritmo:
    - Se o grafo NAO possui arestas de peso negativo -> Dijkstra
      (mais eficiente: O((V + E) log V) com heap binario).
    - Se o grafo possui arestas de peso negativo -> Bellman-Ford
      (O(V * E), mas funciona corretamente com pesos negativos e
      ainda detecta a existencia de ciclos negativos, o que Dijkstra
      nao garante).

Uso:
    python3 roteamento.py <arquivo_entrada> <arquivo_saida>

Exemplo:
    python3 roteamento.py ../dados/grafo_rede_p.txt saida_parte1_p.txt
"""

import heapq
import sys


def ler_grafo(caminho):
    """Le o grafo no formato:
    <num_vertices>\\t<num_arestas>
    <S>\\t<T>
    <u>\\t<v>\\t<custo>   (repetido num_arestas vezes)
    """
    with open(caminho, "r", encoding="utf-8") as f:
        linhas = [linha.rstrip("\n") for linha in f if linha.strip() != ""]

    n, m = map(int, linhas[0].split("\t"))
    s, t = map(int, linhas[1].split("\t"))

    arestas = []
    for i in range(2, 2 + m):
        u, v, custo = linhas[i].split("\t")
        arestas.append((int(u), int(v), float(custo) if "." in custo else int(custo)))

    return n, m, s, t, arestas


def montar_lista_adjacencia(n, arestas):
    adj = [[] for _ in range(n)]
    for u, v, w in arestas:
        adj[u].append((v, w))
    return adj


def dijkstra(n, arestas, origem):
    """Dijkstra classico com heap binario. So deve ser usado quando
    nao ha pesos negativos no grafo."""
    adj = montar_lista_adjacencia(n, arestas)

    dist = [float("inf")] * n
    pred = [-1] * n
    dist[origem] = 0

    fila = [(0, origem)]
    visitado = [False] * n

    while fila:
        d, u = heapq.heappop(fila)
        if visitado[u]:
            continue
        visitado[u] = True

        for v, w in adj[u]:
            novo_custo = dist[u] + w
            if novo_custo < dist[v]:
                dist[v] = novo_custo
                pred[v] = u
                heapq.heappush(fila, (dist[v], v))

    return dist, pred, False  # False = nao ha ciclo negativo (nao se aplica)


def bellman_ford(n, arestas, origem):
    """Bellman-Ford: relaxa todas as arestas (V - 1) vezes. Suporta
    pesos negativos e detecta ciclos negativos com uma rodada extra
    de relaxamento."""
    dist = [float("inf")] * n
    pred = [-1] * n
    dist[origem] = 0

    for _ in range(n - 1):
        houve_atualizacao = False
        for u, v, w in arestas:
            if dist[u] != float("inf") and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                pred[v] = u
                houve_atualizacao = True
        if not houve_atualizacao:
            break  # convergiu antes do limite teorico

    # Rodada extra para detectar ciclo negativo alcancavel a partir da origem
    ciclo_negativo = False
    for u, v, w in arestas:
        if dist[u] != float("inf") and dist[u] + w < dist[v]:
            ciclo_negativo = True
            break

    return dist, pred, ciclo_negativo


def reconstruir_caminho(pred, origem, destino):
    if pred[destino] == -1 and destino != origem:
        return None  # destino inalcancavel

    caminho = []
    atual = destino
    while atual != -1:
        caminho.append(atual)
        if atual == origem:
            break
        atual = pred[atual]
    caminho.reverse()

    if caminho[0] != origem:
        return None
    return caminho


def formatar_custo(valor):
    if isinstance(valor, float) and valor.is_integer():
        return str(int(valor))
    return str(valor)


def resolver(caminho_entrada, caminho_saida):
    n, m, s, t, arestas = ler_grafo(caminho_entrada)

    tem_peso_negativo = any(w < 0 for _, _, w in arestas)

    if tem_peso_negativo:
        algoritmo = "Bellman-Ford"
        justificativa = (
            "O grafo contem arestas com peso negativo (acordos SLA), o que "
            "invalida o uso de Dijkstra. Bellman-Ford suporta pesos "
            "negativos e detecta ciclos negativos."
        )
        dist, pred, ciclo_negativo = bellman_ford(n, arestas, s)
    else:
        algoritmo = "Dijkstra"
        justificativa = (
            "Todos os pesos das arestas sao nao-negativos, portanto "
            "Dijkstra e aplicavel e mais eficiente que Bellman-Ford "
            "(O((V+E) log V) contra O(V*E))."
        )
        dist, pred, ciclo_negativo = dijkstra(n, arestas, s)

    if ciclo_negativo:
        with open(caminho_saida, "w", encoding="utf-8") as f:
            f.write(f"ALGORITMO: {algoritmo}\n")
            f.write(
                "JUSTIFICATIVA: Foi detectado um ciclo de peso negativo "
                "alcancavel a partir da origem; o caminho minimo nao esta "
                "definido.\n"
            )
            f.write("ROTA: -\n")
            f.write("CUSTO: -inf\n")
        print(f"[{caminho_entrada}] Ciclo negativo detectado! Saida gravada em {caminho_saida}")
        return

    caminho = reconstruir_caminho(pred, s, t)

    if caminho is None:
        with open(caminho_saida, "w", encoding="utf-8") as f:
            f.write(f"ALGORITMO: {algoritmo}\n")
            f.write(f"JUSTIFICATIVA: {justificativa}\n")
            f.write("ROTA: -\n")
            f.write("CUSTO: inf\n")
        print(f"[{caminho_entrada}] Destino inalcancavel! Saida gravada em {caminho_saida}")
        return

    custo_total = dist[t]

    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.write(f"ALGORITMO: {algoritmo}\n")
        f.write(f"JUSTIFICATIVA: {justificativa}\n")
        f.write(f"ROTA: {' '.join(map(str, caminho))}\n")
        f.write(f"CUSTO: {formatar_custo(custo_total)}\n")

    print(f"[{caminho_entrada}] {algoritmo} | rota: {caminho} | custo: {formatar_custo(custo_total)}")
    print(f"  -> saida gravada em {caminho_saida}")


def main():
    if len(sys.argv) != 3:
        print("Uso: python3 roteamento.py <arquivo_entrada> <arquivo_saida>")
        sys.exit(1)

    resolver(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
