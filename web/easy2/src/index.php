<?php
    $flag = "flag{n07HIn9_C4N_83_HiDD3n_Fr0m_4_h4X0R}";
    $admin_status = $_POST["is_admin"];
    if(isset($admin_status)){
        if($admin_status == true){
            print $flag;
        }
    }
?>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/css/bootstrap.min.css" />
<div class="container">
    <h1>Login</h1>
    <form action="index.php" method="post">
        Username: <input type="text" name="username" id="" value="admin" /> <br />
        Password: <input type="password" name="password" id="" value="admin" /> <br />
        <input type="hidden" name="is_admin" id="" value=0 />
        <input type="submit" name="" id="" value="submit" />
    </form>
</div>

    
