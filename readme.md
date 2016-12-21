# sadcat

My ssh config is hell. Even if its not much, its hell. I have ~190 host
entries which results in 1094(!) lines of sshconfig.

Why is that?

I use a lot of aliases to remember all my hosts. A typical entry looked
like

```
Host nyc-cexapsdrap21.company.com drap21 pdrap21
  Hostname nyc-cexapsdrap21.company.com
  User myuser
  Port 22
  IdentiyFile ~/.ssh/project_id_rsa
```

You can do a lot of stuff with wildcards in sshconfig. What you cant do is
having dynamic aliases (at least what i know). This would require
a templating like option.

And thats why i wrote this tiny script.


