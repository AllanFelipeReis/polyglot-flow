<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Polyglot Flow | Portal</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container mt-5">
        <div class="card shadow">
            <div class="card-header bg-primary text-white">Criar Novo Pedido (PHP BFF)</div>
            <div class="card-body">
                @if(session('success')) <div class="alert alert-success">{{ session('success') }}</div> @endif
                @if(session('error')) <div class="alert alert-danger">{{ session('error') }}</div> @endif

                <form action="{{ route('orders.store') }}" method="POST">
                    @csrf
                    <div class="mb-3">
                        <label>E-mail do Cliente</label>
                        <input type="email" name="customerEmail" class="form-control" required placeholder="senior@dev.com">
                    </div>
                    <div class="mb-3">
                        <label>Valor do Pedido</label>
                        <input type="number" name="amount" class="form-control" required placeholder="7000.00">
                    </div>
                    <button type="submit" class="btn btn-success w-100">Enviar para o Java</button>
                </form>
            </div>
        </div>
    </div>
</body>
</html>