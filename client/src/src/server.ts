let server_url;

// @ts-ignore
switch (import.meta.env.MODE) {
    case "development":
        server_url = "http://localhost:8000";
    break;
    case "production":
        server_url = "http://104.197.141.191";
    break;
}

export { server_url };
