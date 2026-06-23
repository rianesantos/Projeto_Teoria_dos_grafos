# Comparativo de Algoritmos

## Parte 1 — Roteamento em Rede de Backbone

| Característica | Dijkstra | Bellman-Ford | Floyd-Warshall |
|---|---|---|---|
| Suporta pesos negativos | Não | Sim | Sim |
| Detecta ciclo negativo | Não | Sim | Sim |
| Complexidade | \(O((V+E)\log V)\) com heap | \(O(V \cdot E)\) | \(O(V^3)\) |
| Resolve | 1 origem → todos os destinos | 1 origem → todos os destinos | Todos os pares |
| Quando usar | Pesos não-negativos, grafo esparso | Pesos podem ser negativos | Precisa de todos os pares de distâncias |

**`grafo_rede_p.txt`** — todas as arestas têm peso não-negativo, e o problema pede apenas
o caminho de uma origem (`S`) a um destino (`T`). **Dijkstra** é a escolha mais eficiente
nesse cenário, já que Bellman-Ford e Floyd-Warshall fariam trabalho desnecessário
(o primeiro relaxando arestas repetidamente sem necessidade, o segundo calculando todos
os pares quando só um é pedido).

- Resultado: rota `0 1 3 4`, custo `7`.

**`grafo_rede_m.txt`** — esse grafo contém arestas com custo negativo (representando os
acordos de SLA descritos no enunciado), o que **inviabiliza o uso de Dijkstra**: o
algoritmo assume que, uma vez que um vértice é "fechado" com a menor distância
encontrada, nenhuma aresta futura poderá reduzir esse valor — premissa que pesos
negativos quebram, podendo levar a respostas incorretas. Por isso usamos
**Bellman-Ford**, que relaxa todas as arestas \(V-1\) vezes e, com uma rodada extra de
verificação, também detecta a presença de ciclos negativos alcançáveis a partir da
origem (não detectado nesse grafo). Floyd-Warshall também suportaria pesos negativos,
mas seria desperdício computacional já que o problema pede apenas uma rota `S → T`,
não todos os pares.

- Resultado: rota `0 1 2 4 3 6 9`, custo `6`.

---

## Parte 2 — Alocação de Canais Wi-Fi

| Característica | Guloso simples | DSatur | Backtracking exato |
|---|---|---|---|
| Garante χ(G) ótimo | Não | Não (em geral) | Sim |
| Complexidade | \(O(V + E)\) | \(O(V^2)\) | Exponencial (pior caso) |
| Qualidade típica | Pode usar muito mais cores que o ótimo | Próximo do ótimo na prática | Ótimo garantido |

O enunciado exige o **menor número possível de canais** (o número cromático exato
\(\chi(G)\)), não apenas uma coloração válida qualquer. Tanto o algoritmo guloso simples
quanto o DSatur são heurísticas: produzem rapidamente uma coloração válida, mas **não
garantem otimalidade** — apenas um limite superior para \(\chi(G)\).

Por isso, a solução implementada usa **backtracking exato**: testamos se o grafo pode
ser colorido com \(k = 1, 2, 3, \dots\) cores, parando no menor \(k\) viável. Para reduzir
o espaço de busca, os vértices são ordenados por grau decrescente antes do
backtracking (heurística que tende a podar ramos inválidos mais cedo, no mesmo
espírito do DSatur, mas sem abrir mão da garantia de otimalidade). Como os grafos de
entrada são pequenos/médios, essa abordagem é computacionalmente viável.

- `grafo_wifi_p.txt`: \(\chi(G) = 3\) — coloração `0=1 1=2 2=3 3=1 4=2`.
- `grafo_wifi_m.txt`: \(\chi(G) = 3\) — coloração `0=1 1=2 2=3 3=1 4=2 5=1 6=2 7=1`.

Em ambos os casos o grafo contém triângulos (subgrafos completos \(K_3\)), o que
implica \(\chi(G) \geq 3\); como uma coloração válida com 3 cores foi encontrada, o
backtracking confirma que \(\chi(G) = 3\) é exatamente o ótimo.
