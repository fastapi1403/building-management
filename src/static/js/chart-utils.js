// Chart Utilities
function createChart(canvasId, data, options) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    return new Chart(ctx, {
        data: data,
        options: options
    });
}
