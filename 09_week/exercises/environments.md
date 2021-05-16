# Use conda environment in jupyter

## Register environment/kernel
*https://stackoverflow.com/a/53546675*

```
$ conda activate cenv
(cenv)$ conda install ipykernel
(cenv)$ ipython kernel install --user --name=<any_name_for_kernel>
(cenv)$ conda deactivate
```

This should work with virtual envs too.

## Unregister environment/kernel

*https://stackoverflow.com/a/42647666*

```
jupyter kernelspec list
jupyter kernelspec uninstall <unwanted-kernel>
```
