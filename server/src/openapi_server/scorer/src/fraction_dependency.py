import pkg_resources # pragma: no cover


def fraction_dependency(dependency_list):
    num_dependency = len(dependency_list)
    if num_dependency == 0:
        return 1

    num_required_dependency = 0
        
    for dep in dependency_list.keys():
        dep_segs = dependency_list[dep].split(".")
        if len(dep_segs) >= 2:
            major = dep_segs[0]
            minor = dep_segs[1]
            num_required_dependency += 1

    result = '%0.1f' % float(float(num_required_dependency)/float(num_dependency))
    return result
