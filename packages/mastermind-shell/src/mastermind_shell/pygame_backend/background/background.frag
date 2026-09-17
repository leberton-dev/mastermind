#version 330

uniform float u_time;
uniform vec2 u_resolution;

in vec2 uv;
out vec4 fragColor;

float noise(vec2 p)
{
    return fract(
        sin(dot(p, vec2(127.1, 311.7))) *
        43758.5453123
    );
}

void main()
{
    // Coordonnées centrées
    vec2 p = uv - 0.5;

    // Corriger le ratio de l'écran
    p.x *= u_resolution.x / u_resolution.y;

    float radius = length(p);
    float angle = atan(p.y, p.x);

    // =========================
    // SWIRL
    // =========================

    angle += radius * 5.0;

    // Animation
    angle += u_time * 0.15;

    vec2 swirl = vec2(
        cos(angle),
        sin(angle)
    ) * radius;

    // =========================
    // VAGUES
    // =========================

    float waves =
        sin(swirl.x * 8.0 + u_time * 0.7) *
        0.5 +
        0.5;

    waves +=
        sin(swirl.y * 6.0 - u_time * 0.4) *
        0.5 +
        0.5;

    waves *= 0.5;

    // =========================
    // NOISE
    // =========================

    float n = noise(swirl * 5.0 + u_time * 0.05);

    float value = mix(waves, n, 0.25);

    // =========================
    // COULEURS
    // =========================

    vec3 darkGreen = vec3(
        0.015,
        0.06,
        0.025
    );

    vec3 green = vec3(
        0.05,
        0.35,
        0.12
    );

    vec3 brightGreen = vec3(
        0.25,
        0.8,
        0.25
    );

    vec3 color;

    color = mix(
        darkGreen,
        green,
        smoothstep(0.2, 0.55, value)
    );

    color = mix(
        color,
        brightGreen,
        smoothstep(0.55, 0.9, value)
    );

    // Vignette
    float vignette = 1.0 - radius * 0.8;
    color *= vignette;

    fragColor = vec4(color, 1.0);
}

