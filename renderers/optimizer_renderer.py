from renderers.page_renderer import (
    build_standalone_page,
)


def build_optimizer_page(
    optimizer_result_html=""
):
    body = f"""
<h2>
Evolutionary Optimizer
</h2>

<p>
Run optimization passes against an FLD system design.
</p>

<form method="POST"
action="/optimizer/run">

<label>
Population Size
</label>

<input
type="number"
name="population_size"
value="12"
min="2"
max="200">

<label>
Generations
</label>

<input
type="number"
name="generations"
value="12"
min="1"
max="500">

<label>
Mutation Rate
</label>

<input
type="number"
step="0.01"
name="mutation_rate"
value="0.15">

<label>
Max Budget
</label>

<input
type="number"
name="max_budget"
value="4000">

<br>
<br>

<button type="submit">
Run Optimizer
</button>

</form>

<div class="result">
{optimizer_result_html}
</div>
"""

    return build_standalone_page(
        "Optimizer",
        body
    )
