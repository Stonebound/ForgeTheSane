import data_setup
import os
import json
from shutil import copyfile, copytree
from zipfile import ZipFile

def make_instance(installer_jar):
    print('Making instance for ' + data_setup.forgeversionname)
    
    forgeversionname = data_setup.forgeversionname
    fversionsplit = forgeversionname.split('-')
    mcpversionname = data_setup.mcpversionname
    mcversion = data_setup.mcversion
    shortfversion = mcversion+'-'+fversionsplit[2]
    
    base = os.path.join('instances', forgeversionname)
    data = os.path.join('data', forgeversionname)
    
    # TODO: cleanup this mess
    if not os.path.exists(base):
        libs = os.path.join(base, 'libraries')
        instance = os.path.join(base, 'instances', forgeversionname)
        
        os.makedirs(instance, exist_ok=True)
        os.makedirs(libs, exist_ok=True)
        
        mcclientfolder = os.path.join('net', 'minecraft', 'client')
        copytree(os.path.join(data, mcclientfolder), os.path.join(libs, mcclientfolder))
        
        forgefolder = os.path.join('net', 'minecraftforge', 'forge')
        copytree(os.path.join(data, forgefolder), os.path.join(libs, forgefolder))
        
        clientjar = 'forge-'+shortfversion+'-client.jar'
        copyfile(os.path.join(data, clientjar), os.path.join(libs, forgefolder, shortfversion, clientjar ))
        
        instancecfg = open(os.path.join(instance, "instance.cfg"), "w") 
        instancecfg.write("name=Forge "+mcversion+' '+fversionsplit[2]+'\nInstanceType=OneSix')
        instancecfg.close() 
        
        patches = os.path.join(instance, 'patches')
        os.makedirs(patches, exist_ok=True)
        instancelibs = os.path.join(instance, 'libraries')
        os.makedirs(instancelibs, exist_ok=True)
        
        with ZipFile(installer_jar, 'r') as archive:
            with archive.open('version.json') as prof:
                versions_json = json.loads(prof.read().decode('UTF-8'))
            with archive.open('maven/net/minecraftforge/forge/'+shortfversion+'/forge-'+shortfversion+'.jar') as prof:
                with open(os.path.join(instancelibs, 'forge-'+shortfversion+'.jar'), 'wb') as f:
                    f.write(prof.read())
                
        data = {}
        data['formatVersion'] = 1
        data['name'] = 'Forge'
        data['uid'] = 'net.minecraftforge'
        data['version'] = shortfversion
        data['mainClass'] = 'cpw.mods.modlauncher.Launcher'
        data['requires'] = []
        data['requires'].append({
            'uid': 'net.minecraft',
            'equals': mcversion,
        })
        data['minecraftArguments'] = '--username ${auth_player_name} --version ${version_name} --gameDir ${game_directory} --assetsDir ${assets_root} --assetIndex ${assets_index_name} --uuid ${auth_uuid} --accessToken ${auth_access_token} --userType ${user_type} --versionType ${version_type} --launchTarget fmlclient --fml.forgeVersion '+fversionsplit[2]+' --fml.mcVersion '+mcversion+' --fml.forgeGroup net.minecraftforge --fml.mcpVersion '+mcpversionname.strip("'")+''
        data['libraries'] = versions_json['libraries']
        data['libraries'].pop(0)
        localforge = {
            'name': 'net.minecraftforge:forge:'+shortfversion,
            'MMC-hint': 'local',
        }
        data['libraries'].insert(0, localforge)
        
        with open(os.path.join(patches, "net.minecraftforge.json"), "w") as patchesFile:
            json.dump(data, patchesFile, indent=4)
            
    else:
        print("instance already exists!")
    