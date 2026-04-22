import json
from time import perf_counter

from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods

from .algorithms import (
    bfs,
    bubble_sort,
    dfs,
    dijkstra,
    insertion_sort,
    knapsack,
    lcs,
    merge_sort,
    quick_sort,
    selection_sort,
)
from .models import RunHistory


@require_GET
def index(request):
    return render(request, "visualizer/algorithm-visualizer.html")


@require_GET
def health(request):
    return JsonResponse({"status": "ok"})


def parse_json_body(request):
    try:
        return json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON body")


def parse_int_list(value, field_name):
    if not isinstance(value, list):
        raise ValueError(f"{field_name} must be a list")
    try:
        return [int(x) for x in value]
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} must contain only integers")


def log_run(category, algorithm, input_payload, output_payload, duration_ms):
    run = RunHistory.objects.create(
        category=category,
        algorithm=algorithm,
        input_payload=input_payload,
        output_payload=output_payload,
        duration_ms=duration_ms,
    )
    return run.id


@require_http_methods(["POST"])
@csrf_exempt
def sort_endpoint(request, algo):
    try:
        body = parse_json_body(request)
        arr = parse_int_list(body.get("array", []), "array")

        algorithms = {
            "bubble": bubble_sort,
            "selection": selection_sort,
            "insertion": insertion_sort,
            "merge": merge_sort,
            "quick": quick_sort,
        }
        if algo not in algorithms:
            return JsonResponse({"error": "Unsupported sorting algorithm"}, status=404)

        started = perf_counter()
        sorted_array = algorithms[algo](arr)
        duration_ms = round((perf_counter() - started) * 1000, 3)
        output_payload = {
            "algorithm": algo,
            "input": arr,
            "sorted": sorted_array,
            "duration_ms": duration_ms,
        }
        run_id = log_run("sort", algo, {"array": arr}, output_payload, duration_ms)
        return JsonResponse({
            **output_payload,
            "run_id": run_id,
        })
    except ValueError as exc:
        return HttpResponseBadRequest(str(exc))


@require_http_methods(["POST"])
@csrf_exempt
def graph_endpoint(request, algo):
    try:
        body = parse_json_body(request)
        n = int(body.get("node_count", 0))
        start = int(body.get("start", 0))
        edges = body.get("edges", [])

        if n <= 0:
            raise ValueError("node_count must be greater than 0")
        if not (0 <= start < n):
            raise ValueError("start must be in range [0, node_count)")
        if not isinstance(edges, list):
            raise ValueError("edges must be a list")

        normalized_edges = []
        for edge in edges:
            if not isinstance(edge, list) or len(edge) not in (2, 3):
                raise ValueError("Each edge must be [u, v] or [u, v, w]")
            u = int(edge[0])
            v = int(edge[1])
            w = int(edge[2]) if len(edge) == 3 else 1
            if not (0 <= u < n and 0 <= v < n):
                raise ValueError("Edge vertices must be in range [0, node_count)")
            if w < 0:
                raise ValueError("Edge weight must be non-negative")
            normalized_edges.append([u, v, w])

        started = perf_counter()
        if algo == "bfs":
            order = bfs(n, normalized_edges, start)
            duration_ms = round((perf_counter() - started) * 1000, 3)
            output_payload = {"algorithm": algo, "order": order, "duration_ms": duration_ms}
            run_id = log_run("graph", algo, body, output_payload, duration_ms)
            return JsonResponse({**output_payload, "run_id": run_id})
        if algo == "dfs":
            order = dfs(n, normalized_edges, start)
            duration_ms = round((perf_counter() - started) * 1000, 3)
            output_payload = {"algorithm": algo, "order": order, "duration_ms": duration_ms}
            run_id = log_run("graph", algo, body, output_payload, duration_ms)
            return JsonResponse({**output_payload, "run_id": run_id})
        if algo == "dijkstra":
            result = dijkstra(n, normalized_edges, start)
            duration_ms = round((perf_counter() - started) * 1000, 3)
            output_payload = {"algorithm": algo, **result, "duration_ms": duration_ms}
            run_id = log_run("graph", algo, body, output_payload, duration_ms)
            return JsonResponse({**output_payload, "run_id": run_id})

        return JsonResponse({"error": "Unsupported graph algorithm"}, status=404)
    except ValueError as exc:
        return HttpResponseBadRequest(str(exc))


@require_http_methods(["POST"])
@csrf_exempt
def knapsack_endpoint(request):
    try:
        body = parse_json_body(request)
        weights = parse_int_list(body.get("weights", []), "weights")
        values = parse_int_list(body.get("values", []), "values")
        capacity = int(body.get("capacity", 0))

        if len(weights) != len(values):
            raise ValueError("weights and values must have the same length")
        if capacity < 0:
            raise ValueError("capacity must be non-negative")
        if any(w < 0 for w in weights):
            raise ValueError("weights must be non-negative")

        started = perf_counter()
        result = knapsack(weights, values, capacity)
        duration_ms = round((perf_counter() - started) * 1000, 3)
        output_payload = {**result, "duration_ms": duration_ms}
        run_id = log_run("dp", "knapsack", body, output_payload, duration_ms)
        return JsonResponse({**output_payload, "run_id": run_id})
    except ValueError as exc:
        return HttpResponseBadRequest(str(exc))


@require_http_methods(["POST"])
@csrf_exempt
def lcs_endpoint(request):
    try:
        body = parse_json_body(request)
        s1 = str(body.get("s1", ""))
        s2 = str(body.get("s2", ""))
        started = perf_counter()
        result = lcs(s1, s2)
        duration_ms = round((perf_counter() - started) * 1000, 3)
        output_payload = {**result, "duration_ms": duration_ms}
        run_id = log_run("dp", "lcs", body, output_payload, duration_ms)
        return JsonResponse({**output_payload, "run_id": run_id})
    except ValueError as exc:
        return HttpResponseBadRequest(str(exc))


@require_http_methods(["POST"])
@csrf_exempt
def sort_benchmark_endpoint(request):
    try:
        body = parse_json_body(request)
        arr = parse_int_list(body.get("array", []), "array")
        algorithms = {
            "bubble": bubble_sort,
            "selection": selection_sort,
            "insertion": insertion_sort,
            "merge": merge_sort,
            "quick": quick_sort,
        }

        timings = []
        for name, func in algorithms.items():
            started = perf_counter()
            sorted_arr = func(arr)
            duration_ms = round((perf_counter() - started) * 1000, 3)
            timings.append({
                "algorithm": name,
                "duration_ms": duration_ms,
                "sorted": sorted_arr,
            })

        timings.sort(key=lambda x: x["duration_ms"])
        output_payload = {"input": arr, "timings": timings}
        duration_total_ms = round(sum(item["duration_ms"] for item in timings), 3)
        run_id = log_run("sort", "benchmark", {"array": arr}, output_payload, duration_total_ms)
        return JsonResponse({**output_payload, "run_id": run_id, "duration_ms": duration_total_ms})
    except ValueError as exc:
        return HttpResponseBadRequest(str(exc))


@require_GET
def history_endpoint(request):
    try:
        limit = int(request.GET.get("limit", 12))
    except ValueError:
        return HttpResponseBadRequest("limit must be an integer")

    limit = max(1, min(limit, 100))
    rows = RunHistory.objects.all()[:limit]
    runs = [
        {
            "id": run.id,
            "category": run.category,
            "algorithm": run.algorithm,
            "duration_ms": run.duration_ms,
            "created_at": run.created_at.isoformat(),
        }
        for run in rows
    ]
    return JsonResponse({"count": len(runs), "runs": runs})
