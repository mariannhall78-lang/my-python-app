<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Cloud App</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f172a, #1e293b);
            color: #f8fafc;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            padding: 2.5rem;
            border-radius: 16px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.1);
            text-align: center;
            max-width: 400px;
        }
        h1 {
            color: #38bdf8;
            margin-top: 0;
        }
        p {
            color: #94a3b8;
            font-size: 1.1rem;
            line-height: 1.6;
        }
        .btn {
            display: inline-block;
            background: #38bdf8;
            color: #0f172a;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            text-decoration: none;
            font-weight: bold;
            margin-top: 1rem;
            transition: background 0.2s;
        }
        .btn:hover {
            background: #0ea5e9;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>Welcome to Azure!</h1>
        <p>Your Python application has been successfully configured, built, and deployed using CI/CD pipelines.</p>
        <a href="#" class="btn">Explore App</a>
    </div>
</body>
</html>
